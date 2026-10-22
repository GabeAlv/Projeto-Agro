"""Single demo snapshot shared by the sensor, report and notification pages.

The existing dashboard uses mock_data and the SQLite sensor_readings table is
empty. These values are therefore explicitly sample data, never live readings.
"""
from mock_data import SPATIAL_DATA, TALHAO_DETAIL
from settings_store import load_settings


METRICS = (
    ("air_temp", "Temperatura do ar", "°C"),
    ("soil_humidity", "Umidade do solo", "%"),
    ("air_humidity", "Umidade do ar", "%"),
)


def _series(end, offsets):
    return [round(end + offset, 1) for offset in offsets]


AIR_TEMP_OFFSETS = (-5, -4, -4.5, -3, -2, -2.5, -1, 0, 1, 2, 1, 0.5, 0)
AIR_HUMIDITY_OFFSETS = (9, 8, 10, 6, 4, 2, 3, 0, -3, -1, 1, -2, 0)
SOIL_HUMIDITY_OFFSETS = (7, 6, 6, 5, 4, 3, 3, 2, 1, 0, 1, -1, 0)


def get_devices(settings=None):
    """Return one IoT device per plot, including an offline empty state."""
    readings = {
        "talhao_01": (28, 38, 65),
        "talhao_02": (29, 35, 62),
        "talhao_03": (31, 22, 55),
        "talhao_04": (None, None, None),
    }
    settings = settings if settings is not None else load_settings()
    plots = {plot["id"]: plot for plot in SPATIAL_DATA["talhoes"]}
    devices = []
    for index, source_plot in enumerate(SPATIAL_DATA["talhoes"], 1):
        device_id = f"STS-IOT-{index:02d}"
        config = settings["devices"][device_id]
        plot = plots[config["plot_id"]]
        air_temp, soil_humidity, air_humidity = readings[source_plot["id"]]
        online = air_temp is not None
        devices.append({
            "id": plot["id"],
            "device_id": device_id,
            "nickname": config["nickname"],
            "name": plot["name"].title(),
            "crop": plot["crop"],
            "area": plot["area"],
            "status": (plot["status"] if plot["status"] != "Sensor Offline" else "Sem avaliação") if online else "Sensor Offline",
            "online": online,
            # Fixed demo age, not a timestamp inferred from the machine clock.
            "minutes_since_seen": 5 if online else 45,
            "values": {
                "air_temp": air_temp,
                "soil_humidity": soil_humidity,
                "air_humidity": air_humidity,
            },
            "history": {
                "air_temp": _series(air_temp, AIR_TEMP_OFFSETS) if online else [],
                "soil_humidity": _series(soil_humidity, SOIL_HUMIDITY_OFFSETS) if online else [],
                "air_humidity": _series(air_humidity, AIR_HUMIDITY_OFFSETS) if online else [],
            },
            "detail": TALHAO_DETAIL[plot["id"]],
        })
    return sorted(devices, key=lambda device: device["id"])


def get_notifications(settings=None):
    """Evaluate saved alert rules against the shared demo snapshot."""
    settings = settings if settings is not None else load_settings()
    devices = get_devices(settings)
    rules = settings["alerts"]
    items = []

    def add(device, rule, title, description, severity="Atenção"):
        items.append({
            "id": f'{rule}-{device["device_id"]}', "category": "Alerta", "severity": severity,
            "title": title, "location": device["name"], "description": description,
            "source": "Regra configurada · demonstração", "device_id": device["id"],
        })

    if rules["enabled"]:
        for device in devices:
            if not device["online"]:
                if rules["offline_enabled"] and device["minutes_since_seen"] >= rules["offline_minutes"]:
                    add(device, "offline", "Sensor sem comunicação",
                        f'{device["device_id"]}: sem comunicação há {device["minutes_since_seen"]} min no exemplo. '
                        f'Limite configurado: {rules["offline_minutes"]} min. Verifique o dispositivo.')
                continue
            values = device["values"]
            if rules["temperature_enabled"] and values["air_temp"] > rules["temperature_max"]:
                add(device, "temperature", "Temperatura do ar acima do limite",
                    f'Leitura: {values["air_temp"]:g}°C. Limite: {rules["temperature_max"]:g}°C.', "Crítico")
            if rules["soil_enabled"] and values["soil_humidity"] < rules["soil_min"]:
                add(device, "soil", "Umidade do solo abaixo do limite",
                    f'Leitura: {values["soil_humidity"]:g}%. Limite: {rules["soil_min"]:g}%. '
                    'Confira o solo e o manejo hídrico do talhão.', "Crítico")
            if rules["air_enabled"] and values["air_humidity"] < rules["air_min"]:
                add(device, "air", "Umidade do ar abaixo do limite",
                    f'Leitura: {values["air_humidity"]:g}%. Limite: {rules["air_min"]:g}%.')
    for plot_id, title in (("talhao_02", "Acompanhar umidade"), ("talhao_01", "Conferir leituras")):
        device = next(d for d in devices if d["id"] == plot_id)
        if device["online"]:
            items.append({
                "id": f"tip-{plot_id}", "category": "Indicação", "severity": "Informativo",
                "title": f'{title} no {device["name"]}', "location": device["name"],
                "description": "Acompanhe a evolução das leituras e compare com as condições observadas em campo.",
                "source": "Dados de demonstração do talhão", "device_id": plot_id,
            })
    return items


def format_value(value, unit):
    return "Sem leitura" if value is None else f"{value:g}{unit}"
