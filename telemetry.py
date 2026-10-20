"""Single demo snapshot shared by the sensor, report and notification pages.

The existing dashboard uses mock_data and the SQLite sensor_readings table is
empty. These values are therefore explicitly sample data, never live readings.
"""
from mock_data import SPATIAL_DATA, TALHAO_DETAIL, NOTIFICATIONS_DATA


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


def get_devices():
    """Return one IoT device per plot, including an offline empty state."""
    readings = {
        "talhao_01": (28, 38, 65),
        "talhao_02": (29, 35, 62),
        "talhao_03": (31, 22, 55),
        "talhao_04": (None, None, None),
    }
    devices = []
    for plot in SPATIAL_DATA["talhoes"]:
        air_temp, soil_humidity, air_humidity = readings[plot["id"]]
        online = air_temp is not None
        devices.append({
            "id": plot["id"],
            "device_id": "IMK-IOT-" + plot["id"].split("_")[-1].zfill(2),
            "name": plot["name"].title(),
            "crop": plot["crop"],
            "area": plot["area"],
            "status": plot["status"],
            "online": online,
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
    return devices


def get_notifications():
    """Existing dashboard alerts plus contextual guidance from the same plots."""
    items = []
    for alert in NOTIFICATIONS_DATA["items"]:
        items.append({
            "id": str(alert["id"]),
            "category": "Alerta",
            "severity": "Crítico" if alert["type"] == "critical" else "Atenção",
            "title": alert["title"],
            "location": alert["location"],
            "description": (
                "Verifique o solo e planeje o manejo hídrico do talhão."
                if alert["id"] == 1 else
                "Verifique o gateway IoT e a comunicação do dispositivo antes de confiar nas leituras."
            ),
            "source": alert["source_tag"],
            "device_id": "talhao_03" if alert["id"] == 1 else "talhao_04",
        })
    items.extend([
        {
            "id": "tip-01", "category": "Indicação", "severity": "Informativo",
            "title": "Acompanhar umidade no Talhão Leste 02",
            "location": "Talhão Leste 02",
            "description": "Mantenha a observação da umidade do solo e do alerta fitossanitário registrado no mapa.",
            "source": "Dados do talhão", "device_id": "talhao_02",
        },
        {
            "id": "tip-02", "category": "Indicação", "severity": "Informativo",
            "title": "Conferir leituras do Talhão Norte 01",
            "location": "Talhão Norte 01",
            "description": "Talhão em condição excelente. Use as leituras como referência para acompanhar a evolução.",
            "source": "Dados do talhão", "device_id": "talhao_01",
        },
    ])
    return items


def format_value(value, unit):
    return "Sem leitura" if value is None else f"{value:g}{unit}"
