"""
Componente de Parâmetros Atuais do Clima e Estação Meteorológica.
Herdando de BaseCard.
"""
import flet as ft
from theme import (
    TEXT_WHITE,
    TEXT_MUTED,
    COLOR_WARNING,
)
from mock_data import WEATHER_DATA
from components.base_card import BaseCard


def create_mini_param_item(icon_data, icon_color: str, label: str, value: str) -> ft.Container:
    """Cria um dos 3 sub-cards (Umidade, Vento, Insolação)."""
    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Container(
                    content=ft.Icon(
                        icon=icon_data,
                        size=20,
                        color=icon_color,
                    ),
                    width=36,
                    height=36,
                    border_radius=ft.BorderRadius.all(10),
                    bgcolor="#1a2332",
                    alignment=ft.Alignment.CENTER,
                ),
                ft.Column(
                    controls=[
                        ft.Text(
                            label,
                            size=10.5,
                            color=TEXT_MUTED,
                            weight=ft.FontWeight.W_500,
                        ),
                        ft.Text(
                            value,
                            size=13.5,
                            weight=ft.FontWeight.BOLD,
                            color=TEXT_WHITE,
                        ),
                    ],
                    spacing=1,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            spacing=10,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        bgcolor="#111720",
        border_radius=ft.BorderRadius.all(12),
        padding=ft.Padding.symmetric(horizontal=12, vertical=10),
        border=ft.Border.all(1, "#1e293b"),
        expand=True,
    )


class WeatherCard(BaseCard):
    """Card de Parâmetros Atuais do Clima herdando de BaseCard."""
    def __init__(self, data: dict = WEATHER_DATA, **kwargs):
        # Cabeçalho
        header = ft.Row(
            controls=[
                ft.Text(
                    data["title"],
                    size=13,
                    weight=ft.FontWeight.W_800,
                    color="#cbd5e1",
                ),
                ft.Row(
                    controls=[
                        ft.Icon(
                            icon=ft.Icons.WB_SUNNY_ROUNDED,
                            size=15,
                            color=COLOR_WARNING,
                        ),
                        ft.Text(
                            data["weather_status"],
                            size=12,
                            weight=ft.FontWeight.W_600,
                            color=COLOR_WARNING,
                        ),
                    ],
                    spacing=5,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        # Destaque de Temperatura
        temperature_section = ft.Row(
            controls=[
                ft.Text(
                    data["temperature"],
                    size=40,
                    weight=ft.FontWeight.W_900,
                    color=TEXT_WHITE,
                ),
                ft.Container(
                    content=ft.Text(
                        data["forecast_note"],
                        size=11.5,
                        color=TEXT_MUTED,
                    ),
                    padding=ft.Padding.only(left=8, bottom=4),
                    alignment=ft.Alignment.BOTTOM_LEFT,
                ),
            ],
            vertical_alignment=ft.CrossAxisAlignment.END,
            spacing=6,
        )

        # Linha dos 3 sub-parâmetros
        sub_metrics = ft.Row(
            controls=[
                create_mini_param_item(
                    data["humidity"]["icon"],
                    data["humidity"]["color"],
                    data["humidity"]["label"],
                    data["humidity"]["value"],
                ),
                create_mini_param_item(
                    data["wind"]["icon"],
                    data["wind"]["color"],
                    data["wind"]["label"],
                    data["wind"]["value"],
                ),
                create_mini_param_item(
                    data["insolation"]["icon"],
                    data["insolation"]["color"],
                    data["insolation"]["label"],
                    data["insolation"]["value"],
                ),
            ],
            spacing=10,
        )

        content = ft.Column(
            controls=[
                header,
                ft.Container(height=4),
                temperature_section,
                ft.Container(height=8),
                sub_metrics,
            ],
            spacing=6,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

        super().__init__(
            content=content,
            **kwargs,
        )


def create_weather_card(data: dict = WEATHER_DATA) -> WeatherCard:
    """Factory helper para instanciar o WeatherCard."""
    return WeatherCard(data=data)
