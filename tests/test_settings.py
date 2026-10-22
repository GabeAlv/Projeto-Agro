"""Persistence and cross-page behavior for saved dashboard settings."""
from copy import deepcopy
import json
from pathlib import Path
import tempfile
from types import SimpleNamespace
import unittest
from unittest.mock import Mock, patch

from settings_store import (default_settings, load_settings, save_settings,
                            validate_settings, SettingsValidationError)
from telemetry import get_devices, get_notifications
from pages.settings_page import SettingsPage
from pages.reports_page import ReportsPage
from report_pdf import create_report_pdf
import main as application


class SettingsTests(unittest.TestCase):
    def setUp(self):
        self.directory = tempfile.TemporaryDirectory()
        self.addCleanup(self.directory.cleanup)
        self.path = Path(self.directory.name) / "settings.json"
        self.settings = default_settings()

    def test_defaults_are_independent_and_missing_file_is_not_created(self):
        load_settings(self.path)["property"]["name"] = "Outra propriedade"
        self.assertEqual(load_settings(self.path), self.settings)
        self.assertFalse(self.path.exists())

    def test_round_trip_normalizes_and_is_independent_of_working_directory(self):
        self.settings["property"].update(name="  Fazenda São José  ", location="Uberaba / MG", owner="Ana")
        self.settings["alerts"]["temperature_max"] = "32,5"
        self.settings["preferences"]["initial_route"] = "reports"
        saved = save_settings(self.settings, self.path)
        self.assertEqual(load_settings(self.path), saved)
        self.assertEqual(saved["property"]["name"], "Fazenda São José")
        self.assertEqual(saved["alerts"]["temperature_max"], 32.5)
        self.assertEqual(list(self.path.parent.iterdir()), [self.path])

    def test_invalid_values_preserve_existing_file(self):
        save_settings(self.settings, self.path)
        original = self.path.read_bytes()
        cases = [
            ("property", "name", "  "), ("alerts", "temperature_max", "NaN"),
            ("alerts", "temperature_max", "inf"), ("alerts", "soil_min", -1),
            ("alerts", "air_min", 101), ("alerts", "offline_minutes", 0),
            ("alerts", "offline_minutes", "1.5"), ("alerts", "enabled", "false"),
            ("preferences", "initial_route", "unknown"), ("reports", "default_device", "unknown"),
        ]
        for section, key, value in cases:
            with self.subTest(section=section, key=key, value=value):
                draft = deepcopy(self.settings)
                draft[section][key] = value
                with self.assertRaises(SettingsValidationError):
                    save_settings(draft, self.path)
                self.assertEqual(self.path.read_bytes(), original)

    def test_duplicate_plot_assignments_have_errors_on_both_fields(self):
        self.settings["devices"]["STS-IOT-02"]["plot_id"] = "talhao_01"
        with self.assertRaises(SettingsValidationError) as context:
            validate_settings(self.settings)
        self.assertIn("devices.STS-IOT-01.plot_id", context.exception.errors)
        self.assertIn("devices.STS-IOT-02.plot_id", context.exception.errors)

    def test_failed_atomic_replace_leaves_original_and_no_temp_files(self):
        save_settings(self.settings, self.path)
        original = self.path.read_bytes()
        self.settings["property"]["name"] = "Alterada"
        with patch("settings_store.os.replace", side_effect=PermissionError("blocked")):
            with self.assertRaises(PermissionError):
                save_settings(self.settings, self.path)
        self.assertEqual(self.path.read_bytes(), original)
        self.assertEqual(list(self.path.parent.iterdir()), [self.path])

    def test_invalid_file_falls_back_without_overwriting_and_strict_load_reports_it(self):
        self.path.write_text("{invalid", encoding="utf-8")
        with self.assertLogs("settings_store", level="WARNING"):
            self.assertEqual(load_settings(self.path), self.settings)
        self.assertEqual(self.path.read_text(encoding="utf-8"), "{invalid")
        with self.assertRaises(json.JSONDecodeError):
            load_settings(self.path, strict=True)

    def test_device_swap_moves_readings_alias_and_alerts_together(self):
        self.settings["devices"]["STS-IOT-01"].update(plot_id="talhao_04", nickname="Estação da sede")
        self.settings["devices"]["STS-IOT-04"]["plot_id"] = "talhao_01"
        config = validate_settings(self.settings)
        devices = get_devices(config)
        linked = next(d for d in devices if d["id"] == "talhao_04")
        self.assertEqual(linked["device_id"], "STS-IOT-01")
        self.assertEqual(linked["nickname"], "Estação da sede")
        self.assertEqual(linked["values"]["air_temp"], 28)
        offline = next(n for n in get_notifications(config) if n["id"].startswith("offline-"))
        self.assertEqual(offline["device_id"], "talhao_01")
        self.assertEqual(offline["location"], "Talhão Norte 01")

    def test_alert_toggles_thresholds_and_offline_boundary(self):
        def alerts():
            return [n for n in get_notifications(self.settings) if n["category"] == "Alerta"]
        self.assertEqual(len(alerts()), 2)
        self.settings["alerts"]["enabled"] = False
        self.assertEqual(alerts(), [])
        self.assertTrue(get_notifications(self.settings))  # Indicações remain separate.
        rules = self.settings["alerts"]
        rules.update(enabled=True, soil_min=22, temperature_max=29, air_min=62, offline_minutes=46)
        ids = {n["id"] for n in alerts()}
        self.assertEqual(ids, {"temperature-STS-IOT-03", "air-STS-IOT-03"})
        rules.update(offline_minutes=45, temperature_enabled=False, air_enabled=False)
        self.assertEqual({n["id"] for n in alerts()}, {"offline-STS-IOT-04"})

    def make_editor(self):
        callback = Mock()
        with patch("pages.settings_page.load_settings", return_value=deepcopy(self.settings)):
            editor = SettingsPage(on_saved=callback)
        editor.update = Mock()
        return editor, callback

    def test_form_dirty_discard_restore_and_save(self):
        editor, callback = self.make_editor()
        editor.fields["property.name"].value = "Fazenda Vitória"
        editor._changed()
        self.assertTrue(editor.has_changes)
        self.assertFalse(editor.save_button.disabled)
        editor._discard()
        self.assertFalse(editor.has_changes)
        editor.fields["property.name"].value = "Fazenda Vitória"
        with patch("pages.settings_page.save_settings", side_effect=lambda data: save_settings(data, self.path)):
            editor._save()
        self.assertFalse(editor.has_changes)
        self.assertTrue(editor.save_button.disabled)
        callback.assert_called_once()
        self.assertEqual(load_settings(self.path)["property"]["name"], "Fazenda Vitória")
        editor._restore()
        self.assertTrue(editor.has_changes)
        self.assertEqual(load_settings(self.path)["property"]["name"], "Fazenda Vitória")
        editor._discard()
        self.assertEqual(editor.fields["property.name"].value, "Fazenda Vitória")

    def test_form_errors_and_io_failure_keep_draft(self):
        editor, callback = self.make_editor()
        editor.fields["alerts.offline_minutes"].value = "1.5"
        with patch("pages.settings_page.save_settings", side_effect=lambda data: save_settings(data, self.path)):
            editor._save()
        self.assertIsNotNone(editor.fields["alerts.offline_minutes"].error)
        self.assertFalse(self.path.exists())
        callback.assert_not_called()
        editor.fields["alerts.offline_minutes"].value = "50"
        with patch("pages.settings_page.save_settings", side_effect=PermissionError()):
            editor._save()
        self.assertTrue(editor.has_changes)
        self.assertTrue(editor.feedback.visible)
        self.assertEqual(editor.fields["alerts.offline_minutes"].value, "50")

    def test_report_default_and_snapshot_survive_later_settings_changes(self):
        self.settings["property"].update(name="Fazenda Vitória", location="Uberaba / MG", owner="Marina")
        self.settings["reports"].update(technical_responsible="João da Silva", default_device="talhao_03")
        with patch("pages.reports_page.load_settings", return_value=deepcopy(self.settings)):
            page = ReportsPage()
            page.update = Mock()
            self.assertEqual(page.selected_id, "talhao_03")
            page._generate(SimpleNamespace())
        devices, notifications, generated_at, captured_settings = page.snapshot
        self.assertEqual(len(devices), 1)
        self.assertEqual(devices[0]["id"], "talhao_03")
        self.settings["property"]["name"] = "Outro nome"
        pdf = create_report_pdf(devices, notifications, generated_at, settings=captured_settings)
        self.assertIn("Fazenda Vitória".encode("cp1252"), pdf)
        self.assertIn("João da Silva".encode("cp1252"), pdf)
        self.assertIn(b"Uberaba / MG", pdf)
        self.assertIn(b"Marina", pdf)
        self.assertNotIn(b"Outro nome", pdf)

    def test_initial_route_and_settings_draft_survive_navigation(self):
        self.settings["preferences"]["initial_route"] = "reports"
        page = SimpleNamespace(update=Mock(), add=Mock())
        with patch("main.load_settings", return_value=self.settings):
            application.main(page)
        layout = page.add.call_args.args[0]
        sidebar, content = layout.controls[1].content.controls
        self.assertIsInstance(content.content, ReportsPage)

        def navigate(index):
            sidebar.content.content.controls[1].controls[index].on_click(None)

        navigate(5)
        editor = content.content
        self.assertIsInstance(editor, SettingsPage)
        editor.update = Mock()
        editor.fields["property.name"].value = "Rascunho mantido"
        navigate(0)
        navigate(5)
        self.assertIs(content.content, editor)
        self.assertEqual(editor.fields["property.name"].value, "Rascunho mantido")
        self.assertTrue(editor.has_changes)


if __name__ == "__main__":
    unittest.main()
