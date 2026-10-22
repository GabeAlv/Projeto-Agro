"""Validated, atomic persistence for this installation's dashboard settings."""
from copy import deepcopy
import json
import logging
import math
import os
from pathlib import Path
import tempfile

from mock_data import HEADER_DATA, SPATIAL_DATA


SETTINGS_PATH = Path(__file__).resolve().with_name("user_settings.json")
ROUTES = {
    "dashboard": "Dashboard Geral", "map": "Mapa de Talhões",
    "sensors": "Sensores IoT", "reports": "Relatórios",
    "notifications": "Notificações", "settings": "Configurações",
}
PLOTS = {plot["id"]: plot["name"].title() for plot in SPATIAL_DATA["talhoes"]}
DEFAULTS = {
    "property": {"name": HEADER_DATA["farm_name"], "location": "", "owner": ""},
    "alerts": {
        "enabled": True, "temperature_enabled": True, "temperature_max": 35,
        "soil_enabled": True, "soil_min": 30,
        "air_enabled": True, "air_min": 40,
        "offline_enabled": True, "offline_minutes": 30,
    },
    "devices": {
        f"STS-IOT-{index:02d}": {"nickname": "", "plot_id": plot_id}
        for index, plot_id in enumerate(PLOTS, 1)
    },
    "reports": {"technical_responsible": "", "default_device": "all"},
    "preferences": {"initial_route": "dashboard"},
}


class SettingsValidationError(ValueError):
    def __init__(self, errors):
        self.errors = errors
        super().__init__(next(iter(errors.values())))


def default_settings():
    return deepcopy(DEFAULTS)


def validate_settings(candidate):
    """Return normalized settings; field paths identify errors in the form."""
    if not isinstance(candidate, dict):
        raise SettingsValidationError({"settings": "Formato de configurações inválido."})
    result = default_settings()
    errors = {}
    for section, defaults in DEFAULTS.items():
        values = candidate.get(section, {})
        if not isinstance(values, dict):
            errors[section] = "Seção de configurações inválida."
            continue
        for key in defaults:
            if key in values:
                result[section][key] = deepcopy(values[key])

    text_fields = {
        "property.name": (80, True), "property.location": (100, False),
        "property.owner": (80, False), "reports.technical_responsible": (80, False),
    }
    for path, (maximum, required) in text_fields.items():
        section, key = path.split(".")
        value = result[section][key]
        if not isinstance(value, str):
            errors[path] = "Informe um texto válido."
            continue
        value = " ".join(value.split())
        result[section][key] = value
        if required and not value:
            errors[path] = "Informe o nome da propriedade."
        elif len(value) > maximum:
            errors[path] = f"Use até {maximum} caracteres."

    for key in ("enabled", "temperature_enabled", "soil_enabled", "air_enabled", "offline_enabled"):
        if not isinstance(result["alerts"][key], bool):
            errors[f"alerts.{key}"] = "Escolha ativado ou desativado."
    for key, lower, upper in (("temperature_max", -20, 60), ("soil_min", 0, 100),
                               ("air_min", 0, 100), ("offline_minutes", 1, 1440)):
        try:
            raw = result["alerts"][key]
            if isinstance(raw, bool):
                raise ValueError()
            value = float(str(raw).replace(",", "."))
            if not math.isfinite(value) or not lower <= value <= upper:
                raise ValueError()
            if key == "offline_minutes" and not value.is_integer():
                raise ValueError()
            result["alerts"][key] = int(value) if value.is_integer() else value
        except (ValueError, TypeError):
            errors[f"alerts.{key}"] = (
                "Informe minutos inteiros de 1 a 1440." if key == "offline_minutes"
                else f"Informe um número de {lower} a {upper}."
            )

    assigned = {}
    for device_id, defaults in DEFAULTS["devices"].items():
        device = result["devices"][device_id]
        if not isinstance(device, dict):
            errors[f"devices.{device_id}.plot_id"] = "Dispositivo inválido."
            continue
        device = {**defaults, **device}
        result["devices"][device_id] = device
        nickname = device["nickname"]
        if not isinstance(nickname, str) or len(nickname.strip()) > 40:
            errors[f"devices.{device_id}.nickname"] = "Use um apelido de até 40 caracteres."
        else:
            device["nickname"] = " ".join(nickname.split())
        plot_id = device["plot_id"]
        if not isinstance(plot_id, str) or plot_id not in PLOTS:
            errors[f"devices.{device_id}.plot_id"] = "Selecione um talhão válido."
        elif plot_id in assigned:
            for duplicate in (device_id, assigned[plot_id]):
                errors[f"devices.{duplicate}.plot_id"] = "Cada talhão deve ter um único dispositivo."
        else:
            assigned[plot_id] = device_id
    route = result["preferences"]["initial_route"]
    if not isinstance(route, str) or route not in ROUTES:
        errors["preferences.initial_route"] = "Selecione uma página válida."
    device = result["reports"]["default_device"]
    if not isinstance(device, str) or device not in ("all", *PLOTS):
        errors["reports.default_device"] = "Selecione todos os dispositivos ou um talhão."
    if errors:
        raise SettingsValidationError(errors)
    return result


def load_settings(path=None, *, strict=False):
    path = Path(path) if path is not None else SETTINGS_PATH
    try:
        return validate_settings(json.loads(path.read_text(encoding="utf-8")))
    except FileNotFoundError:
        return default_settings()
    except (OSError, ValueError, TypeError) as exc:
        if strict:
            raise
        logging.getLogger(__name__).warning("Não foi possível ler as configurações: %s", exc)
        return default_settings()


def save_settings(candidate, path=None):
    settings = validate_settings(candidate)
    path = Path(path) if path is not None else SETTINGS_PATH
    temporary = None
    try:
        with tempfile.NamedTemporaryFile(mode="w", encoding="utf-8", dir=path.parent,
                                         prefix=".sts-settings-", suffix=".tmp", delete=False) as stream:
            temporary = Path(stream.name)
            json.dump(settings, stream, ensure_ascii=False, indent=2)
            stream.write("\n")
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary, path)
    finally:
        if temporary is not None and temporary.exists():
            temporary.unlink()
    return settings
