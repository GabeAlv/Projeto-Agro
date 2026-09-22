"""
Card de Detalhes Agronômicos do Talhão Selecionado (Enxuto e sem NDVI).
Herda de BaseCard. Exibe ficha técnica, telemetria de umidade/solo e alertas.
"""
import flet as ft
from theme import (
    TEXT_WHITE,
    TEXT_SECONDARY,
    TEXT_MUTED,
    COLOR_WARNING,
)
from components.base_card import BaseCard
from mock_data import TALHAO_DETAIL


def _info_row(label: str, value: str, value_color: str = TEXT_WHITE) -> ft.Row:
    """Linha de informação label: valor."""
    return ft.Row(
        controls=[
            ft.Text(label, size=11, color=TEXT_MUTED, weight=ft.FontWeight.W_500),
            ft.Text(value, size=11, color=value_color, weight=ft.FontWeight.W_700),
        ],
        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
    )


def _section_title(text: str) -> ft.Text:
    """Título de seção dentro do card."""
    return ft.Text(text, size=10.5, weight=ft.FontWeight.W_800, color="#94a3b8")


def _divider() -> ft.Container:
    """Linha divisória sutil."""
    return ft.Container(height=1, bgcolor="#1e293b")


class TalhaoDetailCard(BaseCard):
    """Painel lateral de detalhes agronômicos do talhão selecionado."""

    def __init__(self, talhao_id: str = "talhao_01", **kwargs):
        data = TALHAO_DETAIL.get(talhao_id, TALHAO_DETAIL["talhao_01"])

        # Cabeçalho do talhão
        header = ft.Row(
            controls=[
                ft.Column(
                    controls=[
                        ft.Text(
                            data["name"],
                            size=14,
                            weight=ft.FontWeight.W_900,
                            color=TEXT_WHITE,
                        ),
                        ft.Row(
                            controls=[
                                ft.Container(
                                    width=8, height=8,
                                    border_radius=ft.BorderRadius.all(4),
                                    bgcolor=data["color"],
                                ),
                                ft.Text(
                                    data["status"],
                                    size=11,
                                    weight=ft.FontWeight.W_600,
                                    color=data["color"],
                                ),
                            ],
                            spacing=6,
                        ),
                    ],
                    spacing=3,
                ),
                ft.Container(
                    content=ft.Text(
                        f"{data['area_ha']} ha",
                        size=11.5,
                        weight=ft.FontWeight.BOLD,
                        color=TEXT_WHITE,
                    ),
                    bgcolor="#111827",
                    padding=ft.Padding.symmetric(horizontal=10, vertical=4),
                    border_radius=ft.BorderRadius.all(8),
                    border=ft.Border.all(1, "#1f2937"),
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.START,
        )

        # Ficha Técnica Enxuta
        ficha = ft.Column(
            controls=[
                _section_title("INFORMAÇÕES GERAIS"),
                _info_row("Cultura", data["crop"]),
                _info_row("Variedade", data["variety"]),
                _info_row("Plantio", data["planting_date"]),
                _info_row("DAP", f"{data['days_after_planting']} dias" if data["days_after_planting"] > 0 else "---"),
            ],
            spacing=4,
        )

        # Umidade e Solo
        umidade = ft.Column(
            controls=[
                _section_title("UMIDADE & TEMPERATURA DO SOLO"),
                _info_row("Profundidade 0-20cm", data["soil_humidity_0_20cm"]),
                _info_row("Profundidade 20-40cm", data["soil_humidity_20_40cm"]),
                _info_row("Temperatura do Solo", data["soil_temp"]),
            ],
            spacing=4,
        )

        # Fitossanitário & Alertas
        fito_items = [
            _section_title("STATUS FITOSSANITÁRIO"),
            ft.Row(
                controls=[
                    ft.Container(
                        width=8, height=8,
                        border_radius=ft.BorderRadius.all(4),
                        bgcolor=data["phytosanitary_color"],
                    ),
                    ft.Text(
                        data["phytosanitary"],
                        size=11,
                        weight=ft.FontWeight.W_600,
                        color=data["phytosanitary_color"],
                    ),
                ],
                spacing=6,
            ),
        ]

        if data["alerts"]:
            for alert_text in data["alerts"]:
                fito_items.append(
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Icon(
                                    icon=ft.Icons.WARNING_AMBER_ROUNDED,
                                    size=13,
                                    color=COLOR_WARNING,
                                ),
                                ft.Text(
                                    alert_text,
                                    size=10,
                                    color="#fbbf24",
                                    weight=ft.FontWeight.W_500,
                                ),
                            ],
                            spacing=5,
                        ),
                        bgcolor="#1c1708",
                        border_radius=ft.BorderRadius.all(6),
                        padding=ft.Padding.symmetric(horizontal=8, vertical=4),
                        border=ft.Border.all(1, "#3a2a12"),
                    )
                )

        fito = ft.Column(controls=fito_items, spacing=4)

        # Último Manejo
        manejo = ft.Column(
            controls=[
                _section_title("ÚLTIMO MANEJO"),
                ft.Text(
                    data["last_management"],
                    size=10.5,
                    color=TEXT_SECONDARY,
                    weight=ft.FontWeight.W_500,
                ),
            ],
            spacing=3,
        )

        # Botões de Ação
        actions = ft.Row(
            controls=[
                ft.Container(
                    content=ft.Text(
                        "Registrar Manejo",
                        size=10.5,
                        weight=ft.FontWeight.W_700,
                        color="#00d2b4",
                    ),
                    bgcolor="#0d2520",
                    border=ft.Border.all(1, "#145040"),
                    border_radius=ft.BorderRadius.all(8),
                    padding=ft.Padding.symmetric(horizontal=12, vertical=6),
                    ink=True,
                ),
                ft.Container(
                    content=ft.Text(
                        "Histórico",
                        size=10.5,
                        weight=ft.FontWeight.W_700,
                        color="#94a3b8",
                    ),
                    bgcolor="#111827",
                    border=ft.Border.all(1, "#1f2937"),
                    border_radius=ft.BorderRadius.all(8),
                    padding=ft.Padding.symmetric(horizontal=12, vertical=6),
                    ink=True,
                ),
            ],
            spacing=8,
        )

        all_controls = [
            header,
            _divider(),
            ficha,
            _divider(),
            umidade,
            _divider(),
            fito,
            _divider(),
            manejo,
            ft.Container(height=2),
            actions,
        ]

        content = ft.Column(
            controls=all_controls,
            spacing=8,
        )

        super().__init__(
            content=content,
            padding=ft.Padding.all(14),
            **kwargs,
        )
