"""
Página de Dashboard Geral do IMK.
Reúne o mapa espacial resumido, parâmetros climáticos, notificações e gráficos de sensores 24h.
"""
import flet as ft
from theme import BG_MAIN
from mock_data import SENSOR_METRICS
from components.map_card import MapCard
from components.weather_card import WeatherCard
from components.alerts_card import AlertsCard
from components.sensor_chart_card import SensorChartCard


class DashboardPage(ft.Container):
    """Página principal do Dashboard Geral."""

    def __init__(self, on_navigate=None, **kwargs):
        # Painel Superior: Mapa Espacial (Esquerda) e Widgets de Clima / Notificações (Direita)
        top_left_map = MapCard(
            on_open_map=lambda: on_navigate("map") if on_navigate else None
        )

        top_right_panel = ft.Container(
            content=ft.Column(
                controls=[
                    WeatherCard(),
                    AlertsCard(),
                ],
                spacing=16,
                alignment=ft.MainAxisAlignment.START,
            ),
            expand=2,
        )

        top_section = ft.Row(
            controls=[
                top_left_map,
                top_right_panel,
            ],
            spacing=16,
            vertical_alignment=ft.CrossAxisAlignment.START,
        )

        # Painel Inferior: 4 Cards de Métricas de Sensores com gráficos 24h
        sensor_cards = [SensorChartCard(sensor=sensor) for sensor in SENSOR_METRICS]

        bottom_section = ft.Row(
            controls=sensor_cards,
            spacing=16,
        )

        # Área de Conteúdo com scroll
        main_content_column = ft.Column(
            controls=[
                top_section,
                ft.Container(height=6),
                bottom_section,
            ],
            spacing=12,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )

        super().__init__(
            content=main_content_column,
            padding=ft.Padding.all(20),
            expand=True,
            bgcolor=BG_MAIN,
            **kwargs,
        )
