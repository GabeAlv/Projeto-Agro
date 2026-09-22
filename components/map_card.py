"""
Componente de Monitoramento Espacial (Mapa de Satélite com Talhões).
Herdando de BaseCard.
"""
import flet as ft
from theme import (
    TEXT_WHITE,
    TEXT_SECONDARY,
    COLOR_GOOD,
)
from mock_data import SPATIAL_DATA
from components.base_card import BaseCard


def create_talhao_box(talhao: dict) -> ft.Container:
    """Cria a marcação retangular do talhão sobre a foto de satélite com suas métricas."""
    header_row = ft.Row(
        controls=[
            ft.Text(
                talhao["name"],
                size=11,
                weight=ft.FontWeight.W_800,
                color=TEXT_WHITE,
            ),
            ft.Text(
                talhao["status"],
                size=11,
                weight=ft.FontWeight.W_600,
                color=talhao["color"],
            ),
        ],
        spacing=8,
        wrap=True,
    )

    sub_info = ft.Text(
        f"Área: {talhao['area']}  |  {talhao['crop']}",
        size=10,
        color="#cbd5e1",
        weight=ft.FontWeight.W_500,
    )

    return ft.Container(
        content=ft.Column(
            controls=[
                header_row,
                sub_info,
            ],
            spacing=3,
        ),
        padding=ft.Padding.all(8),
        border_radius=ft.BorderRadius.all(8),
        border=ft.Border.all(
            1.8,
            talhao["color"],
        ),
        bgcolor="#0f172a88",
        tooltip=f"{talhao['name']}: {talhao['crop']} - {talhao['status']}",
    )


class MapCard(BaseCard):
    """Card de Monitoramento Espacial herdando de BaseCard."""
    def __init__(self, data: dict = SPATIAL_DATA, expand: int | bool = 3, on_open_map=None, **kwargs):
        # Coluna de título
        title_col = ft.Column(
            controls=[
                ft.Text(
                    data["title"],
                    size=16,
                    weight=ft.FontWeight.BOLD,
                    color=TEXT_WHITE,
                ),
                ft.Row(
                    controls=[
                        ft.Text(
                            "Filtro Ativo:",
                            size=11.5,
                            color=TEXT_SECONDARY,
                        ),
                        ft.Text(
                            data["active_filter"],
                            size=11.5,
                            weight=ft.FontWeight.BOLD,
                            color=COLOR_GOOD,
                        ),
                    ],
                    spacing=4,
                ),
            ],
            spacing=2,
        )

        # Badge de coordenadas
        coord_badge = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(
                        icon=ft.Icons.NEAR_ME_ROUNDED,
                        size=14,
                        color=COLOR_GOOD,
                    ),
                    ft.Text(
                        data["coordinates"],
                        size=11,
                        weight=ft.FontWeight.W_600,
                        color="#cbd5e1",
                    ),
                ],
                spacing=6,
            ),
            padding=ft.Padding.symmetric(horizontal=10, vertical=5),
            border_radius=ft.BorderRadius.all(8),
            bgcolor="#111827",
            border=ft.Border.all(1, "#1f2937"),
        )

        # Se houver callback para abrir mapa completo, adiciona botão de ação
        if on_open_map:
            def handle_open(e):
                on_open_map()

            header_actions = ft.Row(
                controls=[
                    coord_badge,
                    ft.Container(
                        content=ft.Row(
                            controls=[
                                ft.Icon(icon=ft.Icons.OPEN_IN_FULL_ROUNDED, size=13, color=COLOR_GOOD),
                                ft.Text("Ver Mapa", size=11, weight=ft.FontWeight.W_700, color=COLOR_GOOD),
                            ],
                            spacing=4,
                        ),
                        bgcolor="#132a28",
                        border=ft.Border.all(1, COLOR_GOOD),
                        border_radius=ft.BorderRadius.all(8),
                        padding=ft.Padding.symmetric(horizontal=8, vertical=5),
                        ink=True,
                        on_click=handle_open,
                        tooltip="Abrir Página Completa de Mapa",
                    ),
                ],
                spacing=8,
            )
        else:
            header_actions = coord_badge

        header = ft.Row(
            controls=[
                title_col,
                header_actions,
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.START,
        )

        # Imagem de fundo do mapa de satélite
        map_background = ft.Image(
            src="assets/satellite_field.png",
            src="assets/drone_crop_field.jpg",
            fit=ft.BoxFit.COVER,
            border_radius=ft.BorderRadius.all(12),
            expand=True,
        )

        # Talhões
        talhoes = data["talhoes"]
        talhao_1 = create_talhao_box(talhoes[0])
        talhao_2 = create_talhao_box(talhoes[1])
        talhao_3 = create_talhao_box(talhoes[2])
        talhao_4 = create_talhao_box(talhoes[3])

        # Montagem do mapa com Stack
        map_view = ft.Container(
            content=ft.Stack(
                controls=[
                    map_background,
                    ft.Container(
                        bgcolor="#00000022",
                        border_radius=ft.BorderRadius.all(12),
                        expand=True,
                    ),
                    ft.Container(
                        content=talhao_1,
                        left=20,
                        top=20,
                        width=230,
                        height=75,
                    ),
                    ft.Container(
                        content=talhao_2,
                        left=265,
                        top=30,
                        width=175,
                        height=75,
                    ),
                    ft.Container(
                        content=talhao_3,
                        left=25,
                        top=140,
                        width=215,
                        height=75,
                    ),
                    ft.Container(
                        content=talhao_4,
                        left=250,
                        top=160,
                        width=200,
                        height=75,
                    ),
                ],
                fit=ft.StackFit.EXPAND,
            ),
            height=320,
            border_radius=ft.BorderRadius.all(12),
            clip_behavior=ft.ClipBehavior.ANTI_ALIAS,
            border=ft.Border.all(1, "#1f2937"),
        )

        content = ft.Column(
            controls=[
                header,
                ft.Container(height=6),
                map_view,
            ],
            spacing=6,
        )

        super().__init__(
            content=content,
            expand=expand,
            **kwargs,
        )


def create_map_card(data: dict = SPATIAL_DATA) -> MapCard:
    """Factory helper para instanciar o MapCard."""
    return MapCard(data=data)
