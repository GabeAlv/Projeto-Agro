"""
Componente de Cabeçalho Superior (Header) do Dashboard.
"""
import flet as ft
from theme import (
    BG_MAIN,
    BORDER_COLOR,
    TEXT_WHITE,
    COLOR_EXCELLENT,
    SYNC_BG,
    SYNC_TEXT,
)
from mock_data import HEADER_DATA
from settings_store import load_settings


def create_header(settings=None) -> ft.Container:
    """Retorna o cabeçalho com a logo STS, status sincronizado e miniatura da fazenda."""
    settings = settings if settings is not None else load_settings()
    farm = settings["property"]
    # Logotipo STS com ícone estilizado
    logo_brand = ft.Row(
        controls=[
            ft.Container(
                content=ft.Icon(
                    icon=ft.Icons.ENERGY_SAVINGS_LEAF_ROUNDED,
                    size=24,
                    color=COLOR_EXCELLENT,
                ),
                width=36,
                height=36,
                border_radius=ft.BorderRadius.all(18),
                bgcolor="#0d2b22",
                border=ft.Border.all(1.5, COLOR_EXCELLENT),
                alignment=ft.Alignment.CENTER,
            ),
            ft.Text(
                HEADER_DATA["system_name"],
                size=22,
                weight=ft.FontWeight.W_900,
                color=TEXT_WHITE,
            ),
        ],
        spacing=12,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    # Badge de sincronização
    sync_badge = ft.Container(
        content=ft.Row(
            controls=[
                ft.Container(
                    width=8,
                    height=8,
                    border_radius=ft.BorderRadius.all(4),
                    bgcolor=SYNC_TEXT,
                ),
                ft.Text(
                    HEADER_DATA["sync_status"],
                    size=12,
                    weight=ft.FontWeight.W_600,
                    color=SYNC_TEXT,
                ),
            ],
            spacing=8,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        bgcolor=SYNC_BG,
        padding=ft.Padding.symmetric(horizontal=14, vertical=6),
        border_radius=ft.BorderRadius.all(16),
        border=ft.Border.all(1, "#144d37"),
    )

    # Miniatura / Avatar da fazenda
    farm_avatar = ft.Container(
        content=ft.Image(
            src="assets/farm_thumb.png",
            fit=ft.BoxFit.COVER,
            width=32,
            height=32,
            border_radius=ft.BorderRadius.all(8),
            error_content=ft.Icon(icon=ft.Icons.GRID_ON_ROUNDED, color=COLOR_EXCELLENT, size=20),
        ),
        width=34,
        height=34,
        border_radius=ft.BorderRadius.all(8),
        border=ft.Border.all(1, "#334155"),
        bgcolor="#1e293b",
        alignment=ft.Alignment.CENTER,
        tooltip=farm["name"],
    )

    right_section = ft.Row(
        controls=[
            sync_badge,
            ft.Container(ft.Column([
                ft.Text(farm["name"], color=TEXT_WHITE, size=12, weight=ft.FontWeight.W_600,
                        max_lines=1, overflow=ft.TextOverflow.ELLIPSIS, tooltip=farm["name"]),
                *([ft.Text(farm["location"], color="#94a3b8", size=10, max_lines=1,
                           overflow=ft.TextOverflow.ELLIPSIS)] if farm["location"] else []),
            ], spacing=2, horizontal_alignment=ft.CrossAxisAlignment.END), width=180),
            farm_avatar,
        ],
        spacing=16,
        vertical_alignment=ft.CrossAxisAlignment.CENTER,
    )

    return ft.Container(
        content=ft.Row(
            controls=[
                logo_brand,
                right_section,
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        bgcolor=BG_MAIN,
        padding=ft.Padding.symmetric(horizontal=24, vertical=12),
        border=ft.Border.only(bottom=ft.BorderSide(1, BORDER_COLOR)),
    )

