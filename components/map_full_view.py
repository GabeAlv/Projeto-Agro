"""
Mapa expandido com imagem de satélite, talhões interativos e ferramentas.
Herda de BaseCard.
"""
import flet as ft
from theme import (
    TEXT_WHITE,
    TEXT_SECONDARY,
    TEXT_MUTED,
    COLOR_GOOD,
)
from components.base_card import BaseCard
from mock_data import SPATIAL_DATA


def _create_talhao_overlay(talhao: dict, on_click_handler=None) -> ft.Container:
    """Cria uma marcação do talhão clicável sobre o mapa."""
    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text(
                            talhao["name"],
                            size=11,
                            weight=ft.FontWeight.W_800,
                            color=TEXT_WHITE,
                        ),
                        ft.Text(
                            talhao["status"],
                            size=10,
                            weight=ft.FontWeight.W_600,
                            color=talhao["color"],
                        ),
                    ],
                    spacing=8,
                    wrap=True,
                ),
                ft.Text(
                    f"Área: {talhao['area']}  |  {talhao['crop']}",
                    size=10,
                    color="#cbd5e1",
                    weight=ft.FontWeight.W_500,
                ),
            ],
            spacing=3,
        ),
        padding=ft.Padding.all(8),
        border_radius=ft.BorderRadius.all(8),
        border=ft.Border.all(2, talhao["color"]),
        bgcolor="#0f172acc",
        tooltip=f"Clique para inspecionar: {talhao['name']}",
        on_click=on_click_handler,
        ink=True,
    )


class MapFullView(BaseCard):
    """Mapa de satélite expandido com talhões interativos e ferramentas."""

    def __init__(
        self,
        on_talhao_click=None,
        selected_talhao_id: str | None = None,
        on_toggle_expand=None,
        is_expanded: bool = False,
        expand: bool | int = True,
        **kwargs,
    ):
        talhoes = SPATIAL_DATA["talhoes"]

        # Handlers para clique nos talhões
        def make_handler(talhao_id):
            def handler(e):
                if on_talhao_click:
                    on_talhao_click(talhao_id)
            return handler

        # Imagem de fundo
        map_bg = ft.Image(
            src="assets/drone_crop_field.jpg",
            src="assets/crop_field.jpg",
            fit=ft.BoxFit.COVER,
            border_radius=ft.BorderRadius.all(12),
            expand=True,
        )

        # Talhões posicionados
        positions = [
            {"left": 25, "top": 25, "width": 240, "height": 75},
            {"left": 290, "top": 35, "width": 210, "height": 75},
            {"left": 30, "top": 150, "width": 235, "height": 75},
            {"left": 290, "top": 175, "width": 220, "height": 75},
        ]

        overlays = [map_bg]
        # Overlay escuro sutil
        overlays.append(
            ft.Container(
                bgcolor="#00000022",
                border_radius=ft.BorderRadius.all(12),
                expand=True,
            )
        )

        for i, talhao in enumerate(talhoes):
            pos = positions[i]
            is_selected = talhao["id"] == selected_talhao_id

            overlay_box = _create_talhao_overlay(
                talhao,
                on_click_handler=make_handler(talhao["id"]),
            )
            # Destaque quando selecionado
            if is_selected:
                overlay_box.border = ft.Border.all(3, TEXT_WHITE)
                overlay_box.bgcolor = "#0f172aee"

            overlays.append(
                ft.Container(
                    content=overlay_box,
                    left=pos["left"],
                    top=pos["top"],
                    width=pos["width"],
                    height=pos["height"],
                )
            )

        # Ferramentas sobrepostas
        # Coordenadas + Altitude
        coord_badge = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(icon=ft.Icons.NEAR_ME_ROUNDED, size=14, color=COLOR_GOOD),
                    ft.Text(
                        f"{SPATIAL_DATA['coordinates']} | Alt: 742m",
                        size=11,
                        weight=ft.FontWeight.W_600,
                        color="#cbd5e1",
                    ),
                ],
                spacing=6,
            ),
            padding=ft.Padding.symmetric(horizontal=10, vertical=6),
            bgcolor="#0c1117ee",
            border_radius=ft.BorderRadius.all(8),
            border=ft.Border.all(1, "#1e293b"),
        )

        # Botão de Ampliar / Reduzir Mapa
        expand_button = None
        if on_toggle_expand:
            def handle_expand_click(e):
                on_toggle_expand()

            expand_icon = ft.Icons.FULLSCREEN_EXIT_ROUNDED if is_expanded else ft.Icons.FULLSCREEN_ROUNDED
            expand_text = "Reduzir Mapa" if is_expanded else "Ampliar Mapa"
            expand_button = ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Icon(icon=expand_icon, size=16, color="#00e676"),
                        ft.Text(expand_text, size=11, weight=ft.FontWeight.BOLD, color="#00e676"),
                    ],
                    spacing=4,
                ),
                padding=ft.Padding.symmetric(horizontal=10, vertical=6),
                bgcolor="#0d2b22ee",
                border_radius=ft.BorderRadius.all(8),
                border=ft.Border.all(1, "#144d37"),
                ink=True,
                on_click=handle_expand_click,
                tooltip="Alternar visualização ampliada do mapa",
            )

        top_tools_row = ft.Row(
            controls=[
                b for b in [coord_badge, expand_button] if b is not None
            ],
            spacing=8,
        )
        overlays.append(ft.Container(content=top_tools_row, right=16, top=16))

        # Bússola / Norte
        compass = ft.Container(
            content=ft.Text("N", size=14, weight=ft.FontWeight.W_900, color=TEXT_WHITE),
            width=32,
            height=32,
            border_radius=ft.BorderRadius.all(16),
            bgcolor="#0c1117dd",
            border=ft.Border.all(1, "#334155"),
            alignment=ft.Alignment.CENTER,
        )
        overlays.append(ft.Container(content=compass, left=16, top=16))

        # Zoom controls
        zoom_col = ft.Column(
            controls=[
                ft.Container(
                    content=ft.Icon(icon=ft.Icons.ADD_ROUNDED, size=18, color="#cbd5e1"),
                    width=32, height=32,
                    border_radius=ft.BorderRadius.all(8),
                    bgcolor="#0c1117dd",
                    border=ft.Border.all(1, "#334155"),
                    alignment=ft.Alignment.CENTER,
                    ink=True,
                ),
                ft.Container(
                    content=ft.Icon(icon=ft.Icons.REMOVE_ROUNDED, size=18, color="#cbd5e1"),
                    width=32, height=32,
                    border_radius=ft.BorderRadius.all(8),
                    bgcolor="#0c1117dd",
                    border=ft.Border.all(1, "#334155"),
                    alignment=ft.Alignment.CENTER,
                    ink=True,
                ),
            ],
            spacing=4,
        )
        overlays.append(ft.Container(content=zoom_col, left=16, bottom=16))

        map_stack = ft.Stack(
            controls=overlays,
            fit=ft.StackFit.EXPAND,
        )

        content = ft.Container(
            content=map_stack,
            border_radius=ft.BorderRadius.all(12),
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            border=ft.Border.all(1, "#1f2937"),
            expand=True,
        )

        super().__init__(
            content=content,
            expand=expand,
            padding=ft.Padding.all(0),
            **kwargs,
        )
