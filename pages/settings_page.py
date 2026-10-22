"""Settings editor; draft changes survive navigation until saved or discarded."""
from copy import deepcopy
import flet as ft

from theme import (BG_MAIN, BORDER_COLOR, TEXT_WHITE, TEXT_MUTED, COLOR_GOOD,
                   COLOR_BLUE, COLOR_WARNING, COLOR_CRITICAL)
from pages.page_ui import heading, panel, label
from settings_store import (ROUTES, PLOTS, default_settings, load_settings,
                            save_settings, validate_settings, SettingsValidationError)


class SettingsPage(ft.Container):
    def __init__(self, on_saved=None, **kwargs):
        self.on_saved = on_saved
        self.fields = {}
        self.load_error = False
        try:
            self.saved = load_settings(strict=True)
        except (OSError, ValueError, TypeError):
            self.saved = default_settings()
            self.load_error = True
        self.status = ft.Text("Tudo salvo", color=COLOR_GOOD, size=12)
        self.feedback = ft.Text("", size=12, visible=False)
        self.save_button = ft.Button("Salvar alterações", icon=ft.Icons.SAVE_OUTLINED,
                                     bgcolor=COLOR_GOOD, color="#06231f", disabled=True,
                                     opacity=0.45, on_click=self._save)
        self.discard_button = ft.TextButton("Descartar alterações", disabled=True, on_click=self._discard)

        property_card = self._section(
            "Propriedade", "Sua fazenda no cabeçalho e nos relatórios.", ft.Icons.GRASS_ROUNDED, [
                self._text("property.name", "Nome da propriedade", max_length=80),
                self._text("property.location", "Localização", hint_text="Município / UF", max_length=100),
                self._text("property.owner", "Responsável pela propriedade", max_length=80),
            ], col={"xs": 12, "lg": 6})
        reports_card = self._section(
            "Relatórios", "Dados usados na prévia e no PDF.", ft.Icons.DESCRIPTION_OUTLINED, [
                self._text("reports.technical_responsible", "Responsável técnico", max_length=80,
                           helper="Opcional. Deixe vazio para omitir no relatório."),
                self._dropdown("reports.default_device", "Seleção padrão do relatório",
                               {"all": "Todos os dispositivos", **PLOTS}),
                label("O nome, a localização e o responsável da propriedade são incluídos automaticamente."),
            ], col={"xs": 12, "lg": 6})
        alerts_card = self._section(
            "Alertas", "Defina quando o dashboard deve chamar sua atenção.", ft.Icons.NOTIFICATIONS_NONE_ROUNDED, [
                self._switch("alerts.enabled", "Habilitar alertas no dashboard e nas notificações"),
                ft.ResponsiveRow([
                    self._alert_rule("temperature_enabled", "Temperatura do ar alta", "temperature_max", "Acima de (°C)"),
                    self._alert_rule("soil_enabled", "Umidade do solo baixa", "soil_min", "Abaixo de (%)"),
                    self._alert_rule("air_enabled", "Umidade do ar baixa", "air_min", "Abaixo de (%)"),
                    self._alert_rule("offline_enabled", "Sensor sem comunicação", "offline_minutes", "A partir de (min)"),
                ], spacing=16, run_spacing=16),
                label("Regras aplicadas aos dados de demonstração. Os limites padrão são exemplos; ajuste ao seu manejo.",
                      COLOR_BLUE),
                label("Na simulação, o sensor STS-IOT-04 está sem comunicação há 45 minutos."),
            ])
        device_cards = []
        for device_id in self.saved["devices"]:
            device_cards.append(ft.Container(ft.Column([
                ft.Row([ft.Icon(ft.Icons.SENSORS_ROUNDED, color=COLOR_GOOD, size=20),
                        label(device_id, TEXT_WHITE, 13)], spacing=8),
                self._text(f"devices.{device_id}.nickname", "Apelido do sensor", max_length=40,
                           hint_text="Ex.: Estação Norte"),
                self._dropdown(f"devices.{device_id}.plot_id", "Talhão vinculado", PLOTS),
            ], spacing=14, horizontal_alignment=ft.CrossAxisAlignment.STRETCH),
                col={"xs": 12, "md": 6, "xl": 3}, padding=16,
                bgcolor="#101720", border=ft.Border.all(1, BORDER_COLOR), border_radius=12))
        devices_card = self._section(
            "Dispositivos", "Identifique seus sensores e organize os vínculos com os talhões.", ft.Icons.MEMORY_ROUNDED, [
                ft.ResponsiveRow(device_cards, spacing=14, run_spacing=14),
                label("Cada talhão recebe um dispositivo. Para trocar vínculos, ajuste os dois sensores antes de salvar."),
                label("Os identificadores dos sensores são fixos. Apelidos e vínculos aparecem nas páginas de sensores e relatórios."),
            ])
        preferences_card = self._section(
            "Preferências", "Personalize a abertura do sistema.", ft.Icons.TUNE_ROUNDED, [
                ft.ResponsiveRow([
                    self._dropdown("preferences.initial_route", "Página inicial", ROUTES,
                                   col={"xs": 12, "md": 6}),
                    ft.Column([label("APARÊNCIA", size=10),
                               ft.Text("Tema escuro STS", color=TEXT_WHITE, size=14),
                               label("Mantém o padrão visual do dashboard.")],
                              spacing=6, col={"xs": 12, "md": 6}),
                ], spacing=20, run_spacing=16),
                label("A página inicial será usada na próxima abertura do sistema."),
            ])
        toolbar = panel(ft.Row([
            ft.Column([self.status, label("Salve para aplicar às outras páginas. O rascunho é mantido ao navegar.")],
                      spacing=4),
            ft.Row([self.discard_button, self.save_button], spacing=10, wrap=True),
        ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, wrap=True, spacing=12), padding=16)
        toolbar.width = float("inf")
        page_heading = heading("Configurações", "Ajustes da propriedade e do monitoramento", ft.Icons.SETTINGS_OUTLINED)
        page_heading.expand = True
        content = ft.Column([
            ft.Row([
                page_heading,
                ft.Container(label("Preferências locais", COLOR_BLUE), bgcolor="#10202d", border_radius=20,
                             padding=ft.Padding.symmetric(horizontal=14, vertical=8)),
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            self.feedback,
            ft.Column([
                ft.ResponsiveRow([property_card, reports_card], spacing=18, run_spacing=18),
                alerts_card, devices_card, preferences_card,
                panel(ft.Row([
                    ft.Column([ft.Text("Restaurar configurações padrão", color=TEXT_WHITE, size=14,
                                       weight=ft.FontWeight.W_600),
                               label("Preenche os valores originais para revisão. Clique em Salvar alterações para aplicar.")],
                              spacing=5),
                    ft.OutlinedButton("Restaurar padrão", icon=ft.Icons.RESTORE_ROUNDED, on_click=self._restore),
                ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN, wrap=True, spacing=16)),
            ], spacing=18, scroll=ft.ScrollMode.AUTO, expand=True,
               horizontal_alignment=ft.CrossAxisAlignment.STRETCH),
            toolbar,
        ], spacing=16, expand=True)
        super().__init__(content=content, padding=20, bgcolor=BG_MAIN, expand=True, **kwargs)
        self._sync_rules()
        if self.load_error:
            self._message("Não foi possível ler as configurações salvas. Revise os valores padrão e salve para recuperar.",
                          COLOR_WARNING)
            self.save_button.disabled = False
            self.save_button.opacity = 1
            self.status.value = "Revisão necessária"
            self.status.color = COLOR_WARNING

    def _value(self, path, settings=None):
        result = self.saved if settings is None else settings
        for part in path.split("."):
            result = result[part]
        return result

    def _text(self, path, title, **kwargs):
        field = ft.TextField(value=str(self._value(path)), label=title, text_size=13,
                             color=TEXT_WHITE, border_color=BORDER_COLOR, focused_border_color=COLOR_GOOD,
                             border_radius=10, dense=True, on_change=self._changed, **kwargs)
        self.fields[path] = field
        return field

    def _dropdown(self, path, title, options, **kwargs):
        field = ft.Dropdown(value=self._value(path), label=title, text_size=13,
                            options=[ft.DropdownOption(key=key, text=text) for key, text in options.items()],
                            border_color=BORDER_COLOR, focused_border_color=COLOR_GOOD,
                            border_radius=10, dense=True, on_select=self._changed, **kwargs)
        self.fields[path] = field
        return field

    def _switch(self, path, title):
        field = ft.Switch(label=title, value=self._value(path), active_color=COLOR_GOOD,
                          label_text_style=ft.TextStyle(size=12, color=TEXT_WHITE), on_change=self._changed)
        self.fields[path] = field
        return field

    def _section(self, title, description, icon, controls, col=12):
        return panel(ft.Column([
            ft.Row([ft.Container(ft.Icon(icon, color=COLOR_GOOD, size=21), width=40, height=40,
                                 bgcolor="#10312d", border_radius=10, alignment=ft.Alignment.CENTER),
                    ft.Column([ft.Text(title, color=TEXT_WHITE, size=17, weight=ft.FontWeight.BOLD),
                               ft.Text(description, color=TEXT_MUTED, size=12)], spacing=3, expand=True)], spacing=12),
            ft.Divider(color=BORDER_COLOR, height=10), *controls,
        ], spacing=16, horizontal_alignment=ft.CrossAxisAlignment.STRETCH), col=col)

    def _alert_rule(self, toggle, title, value_key, value_label):
        field = self._text(f"alerts.{value_key}", value_label, keyboard_type=ft.KeyboardType.NUMBER)
        return ft.Column([self._switch(f"alerts.{toggle}", title), field], spacing=10,
                         col={"xs": 12, "md": 6, "xl": 3}, horizontal_alignment=ft.CrossAxisAlignment.STRETCH)

    def _draft(self):
        draft = default_settings()
        for path, field in self.fields.items():
            parts = path.split(".")
            target = draft
            for part in parts[:-1]:
                target = target[part]
            target[parts[-1]] = field.value
        return draft

    @property
    def has_changes(self):
        try:
            return validate_settings(self._draft()) != self.saved
        except SettingsValidationError:
            return True

    def _sync_rules(self):
        enabled = self.fields["alerts.enabled"].value
        for toggle, value in (("temperature_enabled", "temperature_max"), ("soil_enabled", "soil_min"),
                              ("air_enabled", "air_min"), ("offline_enabled", "offline_minutes")):
            self.fields[f"alerts.{toggle}"].disabled = not enabled
            self.fields[f"alerts.{value}"].disabled = not enabled or not self.fields[f"alerts.{toggle}"].value

    def _clear_errors(self):
        for field in self.fields.values():
            if isinstance(field, ft.TextField):
                field.error = None
            elif isinstance(field, ft.Dropdown):
                field.error_text = None

    def _changed(self, e=None):
        self._clear_errors()
        self.feedback.visible = False
        self._sync_rules()
        dirty = self.has_changes
        self.status.value = "Alterações não salvas" if dirty else "Revisão necessária" if self.load_error else "Tudo salvo"
        self.status.color = COLOR_WARNING if dirty or self.load_error else COLOR_GOOD
        self.save_button.disabled = not (dirty or self.load_error)
        self.save_button.opacity = 0.45 if self.save_button.disabled else 1
        self.discard_button.disabled = not dirty
        self.update()

    def _message(self, text, color):
        self.feedback.value = text
        self.feedback.color = color
        self.feedback.visible = True

    def _fill(self, settings):
        for path, field in self.fields.items():
            value = self._value(path, settings)
            field.value = str(value) if isinstance(field, ft.TextField) else value
        self._changed()

    def _restore(self, e=None):
        self._fill(default_settings())
        self._message("Valores padrão carregados para revisão. Salve para aplicar ou descarte para voltar.", COLOR_BLUE)
        self.update()

    def _discard(self, e=None):
        self._fill(self.saved)

    def _save(self, e=None):
        self._clear_errors()
        try:
            saved = save_settings(self._draft())
        except SettingsValidationError as exc:
            for path, message in exc.errors.items():
                field = self.fields.get(path)
                if isinstance(field, ft.TextField):
                    field.error = message
                elif isinstance(field, ft.Dropdown):
                    field.error_text = message
            self._message("Revise os campos destacados. " + str(exc), COLOR_CRITICAL)
            self.update()
            return
        except OSError:
            self._message("Não foi possível salvar. Confira a permissão de escrita na pasta do dashboard e tente novamente.",
                          COLOR_CRITICAL)
            self.update()
            return
        self.saved = deepcopy(saved)
        self.load_error = False
        self._fill(saved)
        self._message("Configurações salvas. Os ajustes já estão disponíveis nas outras páginas.", COLOR_GOOD)
        if self.on_saved:
            self.on_saved(saved)
        self.update()
