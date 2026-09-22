"""
Dados mockados (chumbados) da aplicação IMK para visualização no frontend.
Estruturado para futura integração facilitada com banco de dados SQLite.
"""
import flet as ft

# Dados do Cabeçalho e Sistema
HEADER_DATA = {
    "system_name": "IMK",
    "sync_status": "Sincronizado",
    "farm_name": "Fazenda Santa Maria",
    "version": "v2.4-agro",
}

# Monitoramento Espacial e Talhões
SPATIAL_DATA = {
    "title": "Monitoramento Espacial",
    "active_filter": "Visão Satélite",
    "coordinates": "19°45'08\"S | 47°55'42\"W",
    "talhoes": [
        {
            "id": "talhao_01",
            "name": "TALHÃO NORTE 01",
            "status": "Excelente",
            "area": "120 ha",
            "crop": "Soja",
            "color": "#00e676",
            "is_dashed": False,
        },
        {
            "id": "talhao_02",
            "name": "TALHÃO LESTE 02",
            "status": "Bom",
            "area": "95 ha",
            "crop": "Milho",
            "color": "#00d2b4",
            "is_dashed": False,
        },
        {
            "id": "talhao_03",
            "name": "TALHÃO SUL 03",
            "status": "Estresse Hídrico",
            "area": "85 ha",
            "crop": "Algodão",
            "color": "#f59e0b",
            "is_dashed": False,
        },
        {
            "id": "talhao_04",
            "name": "TALHÃO OESTE 04",
            "status": "Sensor Offline",
            "area": "80 ha",
            "crop": "Alqueire",
            "color": "#ef4444",
            "is_dashed": True,
        },
    ],
}

# Parâmetros Atuais Climáticos
WEATHER_DATA = {
    "title": "PARÂMETROS ATUAIS",
    "weather_status": "Sol com Nuvens",
    "temperature": "30°C",
    "forecast_note": "Sem previsão de alteração",
    "humidity": {
        "value": "58%",
        "label": "Umidade",
        "icon": ft.Icons.WATER_DROP_ROUNDED,
        "color": "#38bdf8",
    },
    "wind": {
        "value": "12 km/h",
        "label": "Vento",
        "icon": ft.Icons.AIR_ROUNDED,
        "color": "#00d2b4",
    },
    "insolation": {
        "value": "0.4 W/m²",
        "label": "Insolação",
        "icon": ft.Icons.WB_SUNNY_ROUNDED,
        "color": "#f59e0b",
    },
}

# Notificações e Alertas Preditivos
NOTIFICATIONS_DATA = {
    "title": "NOTIFICAÇÕES",
    "badge_text": "Crítico",
    "items": [
        {
            "id": 1,
            "type": "warning",
            "icon": ft.Icons.WARNING_AMBER_ROUNDED,
            "color": "#f59e0b",
            "bg_color": "#2c2010",
            "title": "Alerta de Estresse Hídrico Previsto",
            "location": "Talhão Sul 03",
            "source_tag": "Previsão de ML",
        },
        {
            "id": 2,
            "type": "critical",
            "icon": ft.Icons.ERROR_OUTLINE_ROUNDED,
            "color": "#ef4444",
            "bg_color": "#301518",
            "title": "Queda de Umidade do Solo Prevista",
            "location": "Talhão Oeste 04",
            "source_tag": "Modelo preditivo",
        },
    ],
}

# Métricas Históricas de Sensores (Cards inferiores com gráficos 24h)
SENSOR_METRICS = [
    {
        "id": "air_temp",
        "title": "TEMPERATURA DO AR",
        "icon": ft.Icons.DEVICE_THERMOSTAT_ROUNDED,
        "icon_color": "#f59e0b",
        "reading_label": "Última leitura",
        "value": "28",
        "unit": "°C",
        "trend_val": "+1.2",
        "trend_type": "up",
        "chart_color": "#f59e0b",
        "max_label": "35°C",
        "min_label": "20°C",
        "history": [22, 23.5, 22, 25, 27, 26, 28.5, 27.5, 29.5, 30.5, 28.8, 27.2, 28.0],
    },
    {
        "id": "air_humidity",
        "title": "UMIDADE DO AR",
        "icon": ft.Icons.WATER_DROP_ROUNDED,
        "icon_color": "#38bdf8",
        "reading_label": "Última leitura",
        "value": "65",
        "unit": "%",
        "trend_val": "-3",
        "trend_type": "down",
        "chart_color": "#38bdf8",
        "max_label": "80%",
        "min_label": "30%",
        "history": [74, 71, 75, 68, 66, 62, 64, 59, 57, 61, 65, 63, 65],
    },
    {
        "id": "soil_temp",
        "title": "TEMPERATURA DO SOLO",
        "icon": ft.Icons.DEVICE_THERMOSTAT_ROUNDED,
        "icon_color": "#00e676",
        "reading_label": "Última leitura",
        "value": "24",
        "unit": "°C",
        "trend_val": "+0.8",
        "trend_type": "up",
        "chart_color": "#00e676",
        "max_label": "35°C",
        "min_label": "15°C",
        "history": [19.5, 20.2, 21.0, 20.4, 22.1, 21.5, 23.0, 22.3, 24.5, 23.8, 25.2, 24.3, 24.0],
    },
    {
        "id": "soil_humidity",
        "title": "UMIDADE DO SOLO",
        "icon": ft.Icons.WATER_DROP_ROUNDED,
        "icon_color": "#38bdf8",
        "reading_label": "Última leitura",
        "value": "42",
        "unit": "%",
        "trend_val": "-2",
        "trend_type": "down",
        "chart_color": "#38bdf8",
        "max_label": "80%",
        "min_label": "30%",
        "history": [52, 48, 51, 46, 43, 40, 42, 38, 35, 39, 42, 40, 42],
    },
]

# ──────────────────────────────────────────────────────────────────────────────
# Dados detalhados dos Talhões para a Página do Mapa (Enxuto & Sem NDVI)
# ──────────────────────────────────────────────────────────────────────────────

TALHAO_DETAIL = {
    "talhao_01": {
        "id": "talhao_01",
        "name": "TALHÃO NORTE 01",
        "crop": "Soja",
        "variety": "TMG 2381 IPRO",
        "area_ha": 120,
        "status": "Excelente",
        "color": "#00e676",
        "planting_date": "15/10/2026",
        "days_after_planting": 128,
        "soil_humidity_0_20cm": "38%",
        "soil_humidity_20_40cm": "42%",
        "soil_temp": "24.5°C",
        "phytosanitary": "Saudável",
        "phytosanitary_color": "#00e676",
        "alerts": [],
        "last_management": "Aplicação Fungicida - 28/01/2027",
        "coordinates": "19°44'52\"S | 47°55'38\"W",
        "altitude": "742m",
    },
    "talhao_02": {
        "id": "talhao_02",
        "name": "TALHÃO LESTE 02",
        "crop": "Milho",
        "variety": "DKB 390 PRO3",
        "area_ha": 95,
        "status": "Bom",
        "color": "#00d2b4",
        "planting_date": "05/11/2026",
        "days_after_planting": 107,
        "soil_humidity_0_20cm": "35%",
        "soil_humidity_20_40cm": "40%",
        "soil_temp": "25.1°C",
        "phytosanitary": "Monitorar Cigarrinha",
        "phytosanitary_color": "#f59e0b",
        "alerts": ["Cigarrinha detectada em armadilha"],
        "last_management": "Adubação de Cobertura - 20/01/2027",
        "coordinates": "19°44'58\"S | 47°55'25\"W",
        "altitude": "738m",
    },
    "talhao_03": {
        "id": "talhao_03",
        "name": "TALHÃO SUL 03",
        "crop": "Algodão",
        "variety": "FM 983 GLT",
        "area_ha": 85,
        "status": "Estresse Hídrico",
        "color": "#f59e0b",
        "planting_date": "01/12/2026",
        "days_after_planting": 81,
        "soil_humidity_0_20cm": "22%",
        "soil_humidity_20_40cm": "28%",
        "soil_temp": "27.3°C",
        "phytosanitary": "Estresse Hídrico Confirmado",
        "phytosanitary_color": "#f59e0b",
        "alerts": ["Déficit hídrico identificado nos sensores"],
        "last_management": "Irrigação de Salvamento - 01/02/2027",
        "coordinates": "19°45'15\"S | 47°55'40\"W",
        "altitude": "735m",
    },
    "talhao_04": {
        "id": "talhao_04",
        "name": "TALHÃO OESTE 04",
        "crop": "Pousio (Alqueire)",
        "variety": "---",
        "area_ha": 80,
        "status": "Sensor Offline",
        "color": "#ef4444",
        "planting_date": "---",
        "days_after_planting": 0,
        "soil_humidity_0_20cm": "---",
        "soil_humidity_20_40cm": "---",
        "soil_temp": "---",
        "phytosanitary": "Sensor Offline",
        "phytosanitary_color": "#ef4444",
        "alerts": ["Gateway IoT sem resposta"],
        "last_management": "Dessecação Pré-plantio - 10/09/2026",
        "coordinates": "19°45'22\"S | 47°55'50\"W",
        "altitude": "730m",
    },
}

# Filtros/Camadas disponíveis na Página do Mapa
MAP_LAYER_FILTERS = [
    {"id": "satellite", "label": "Visão Satélite", "active": True},
    {"id": "soil_moisture", "label": "Umidade do Solo (0-40cm)", "active": False},
    {"id": "zoning", "label": "Zoneamento & Variedade", "active": False},
]

# Info geral da fazenda para a página de mapa
FARM_INFO = {
    "name": "Fazenda Santa Maria",
    "season": "Safra 2026/2027",
    "total_area": "380 ha",
    "total_talhoes": 4,
    "coordinates": "19°45'08\"S | 47°55'42\"W",
    "altitude": "742m",
    "municipality": "Uberaba - MG",
}

# Resumo tabular dos talhões para a tabela inferior
TALHOES_TABLE_DATA = [
    {
        "id": "talhao_01",
        "name": "Talhão Norte 01",
        "crop": "Soja",
        "area": "120 ha",
        "status": "Excelente",
        "color": "#00e676",
        "humidity": "38%",
    },
    {
        "id": "talhao_02",
        "name": "Talhão Leste 02",
        "crop": "Milho",
        "area": "95 ha",
        "status": "Bom",
        "color": "#00d2b4",
        "humidity": "35%",
    },
    {
        "id": "talhao_03",
        "name": "Talhão Sul 03",
        "crop": "Algodão",
        "area": "85 ha",
        "status": "Estresse Hídrico",
        "color": "#f59e0b",
        "humidity": "22%",
    },
    {
        "id": "talhao_04",
        "name": "Talhão Oeste 04",
        "crop": "Pousio",
        "area": "80 ha",
        "status": "Sensor Offline",
        "color": "#ef4444",
        "humidity": "---",
    },
]
