"""
Tabela resumida de todos os talhões da safra (Enxuta e sem NDVI).
Herda de BaseCard.
"""
import flet as ft
from theme import (
    TEXT_WHITE,
    TEXT_SECONDARY,
    TEXT_MUTED,
)
from components.base_card import BaseCard
from mock_data import TALHOES_TABLE_DATA


def _status_badge(status: str, color: str) -> ft.Container:
    """Badge compacto de status com cor."""
    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Container(
                    width=7, height=7,
                    border_radius=ft.BorderRadius.all(4),
                    bgcolor=color,
                ),
                ft.Text(
                    status,
                    size=11,
                    weight=ft.FontWeight.W_600,
                    color=color,
                ),
            ],
            spacing=6,
        ),
    )


class TalhoesTableCard(BaseCard):
    """Tabela com resumo operacional de todos os talhões da fazenda."""

    def __init__(self, on_row_click=None, **kwargs):
        # Cabeçalho da tabela
        col_style = {
            "size": 10.5,
            "weight": ft.FontWeight.W_800,
            "color": "#64748b",
        }

        header_row = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Container(content=ft.Text("TALHÃO", **col_style), expand=3),
                    ft.Container(content=ft.Text("CULTURA", **col_style), expand=2),
                    ft.Container(content=ft.Text("ÁREA", **col_style), expand=2),
                    ft.Container(content=ft.Text("STATUS", **col_style), expand=3),
                    ft.Container(content=ft.Text("UMIDADE DO SOLO", **col_style), expand=2),
                ],
                spacing=8,
                vertical_alignment=ft.CrossAxisAlignment.CENTER,
            ),
            padding=ft.Padding.symmetric(horizontal=14, vertical=8),
            border=ft.Border.only(bottom=ft.BorderSide(1, "#1e293b")),
        )

        # Linhas de dados
        data_rows = []
        for talhao in TALHOES_TABLE_DATA:
            def make_handler(tid):
                def handler(e):
                    if on_row_click:
                        on_row_click(tid)
                return handler

            row = ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Row(
                                controls=[
                                    ft.Container(
                                        width=7, height=7,
                                        border_radius=ft.BorderRadius.all(4),
                                        bgcolor=talhao["color"],
                                    ),
                                    ft.Text(
                                        talhao["name"],
                                        size=11.5,
                                        weight=ft.FontWeight.W_600,
                                        color=TEXT_WHITE,
                                    ),
                                ],
                                spacing=8,
                            ),
                            expand=3,
                        ),
                        ft.Container(
                            content=ft.Text(talhao["crop"], size=11.5, color=TEXT_SECONDARY),
                            expand=2,
                        ),
                        ft.Container(
                            content=ft.Text(talhao["area"], size=11.5, color=TEXT_SECONDARY),
                            expand=2,
                        ),
                        ft.Container(
                            content=_status_badge(talhao["status"], talhao["color"]),
                            expand=3,
                        ),
                        ft.Container(
                            content=ft.Text(talhao["humidity"], size=11.5, color=TEXT_SECONDARY),
                            expand=2,
                        ),
                    ],
                    spacing=8,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                padding=ft.Padding.symmetric(horizontal=14, vertical=9),
                border=ft.Border.only(bottom=ft.BorderSide(1, "#111827")),
                ink=True,
                on_click=make_handler(talhao["id"]),
                bgcolor="#141b24",
                on_hover=lambda e: None,
            )
            data_rows.append(row)

        # Título
        title_row = ft.Row(
            controls=[
                ft.Text(
                    "RESUMO DOS TALHÕES",
                    size=13,
                    weight=ft.FontWeight.W_800,
                    color="#cbd5e1",
                ),
                ft.Container(
                    content=ft.Text(
                        f"{len(TALHOES_TABLE_DATA)} talhões",
                        size=10.5,
                        weight=ft.FontWeight.BOLD,
                        color="#64748b",
                    ),
                    bgcolor="#111827",
                    padding=ft.Padding.symmetric(horizontal=8, vertical=3),
                    border_radius=ft.BorderRadius.all(6),
                    border=ft.Border.all(1, "#1f2937"),
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        content = ft.Column(
            controls=[
                title_row,
                ft.Container(height=4),
                header_row,
                *data_rows,
            ],
            spacing=0,
        )

        super().__init__(
            content=content,
            padding=ft.Padding.all(16),
            **kwargs,
        )
