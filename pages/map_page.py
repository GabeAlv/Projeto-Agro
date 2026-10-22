"""
Página do Mapa de Talhões do STS (Enxuta, sem NDVI e com opção de ampliação).
Visão espacial expandida, filtros simplificados, inspetor e tabela.
"""
import flet as ft
from theme import (
    BG_MAIN,
    BG_CARD,
    BORDER_COLOR,
    TEXT_WHITE,
    TEXT_MUTED,
    COLOR_GOOD,
    COLOR_EXCELLENT,
)
from mock_data import FARM_INFO, MAP_LAYER_FILTERS
from components.map_full_view import MapFullView
from components.talhao_detail_card import TalhaoDetailCard
from components.talhoes_table_card import TalhoesTableCard


class MapPage(ft.Container):
    """Página dedicada ao mapa geoespacial da fazenda e gestão de talhões."""

    def __init__(self, **kwargs):
        self.selected_talhao_id = "talhao_01"
        self.active_filter_id = "drone_crop_field"
        self.filters = list(MAP_LAYER_FILTERS)
        self.is_map_expanded = False

        # Container dinâmico do mapa
        self.map_container = ft.Container(
            content=MapFullView(
                on_talhao_click=self._on_talhao_selected,
                selected_talhao_id=self.selected_talhao_id,
                on_toggle_expand=self._toggle_map_expand,
                is_expanded=self.is_map_expanded,
            ),
            expand=True,
            height=430,
        )

        # Container dinâmico dos detalhes do talhão
        self.detail_container = ft.Container(
            content=TalhaoDetailCard(talhao_id=self.selected_talhao_id),
            width=350,
            visible=True,
        )

        # Top Control Bar (Seletor, Camadas e Ações)
        top_bar = self._build_top_control_bar()

        # Seção Central: Mapa + Card de Detalhes
        self.middle_section = ft.Row(
            controls=[
                self.map_container,
                self.detail_container,
            ],
            spacing=16,
            vertical_alignment=ft.CrossAxisAlignment.START,
        )

        # Seção Inferior: Tabela de Talhões
        self.table_container = ft.Container(
            content=TalhoesTableCard(on_row_click=self._on_talhao_selected),
        )

        # Scroll geral da página
        main_column = ft.Column(
            controls=[
                top_bar,
                ft.Container(height=4),
                self.middle_section,
                ft.Container(height=4),
                self.table_container,
            ],
            spacing=12,
            scroll=ft.ScrollMode.AUTO,
            expand=True,
        )

        super().__init__(
            content=main_column,
            padding=ft.Padding.all(20),
            expand=True,
            bgcolor=BG_MAIN,
            **kwargs,
        )

    def _build_filter_pill(self, filter_item: dict) -> ft.Container:
        """Cria um botão de filtro estilo pill."""
        is_active = filter_item["id"] == self.active_filter_id

        def on_click(e):
            self.active_filter_id = filter_item["id"]
            self._refresh_filters()

        if is_active:
            return ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Container(
                            width=6, height=6,
                            border_radius=ft.BorderRadius.all(3),
                            bgcolor=COLOR_GOOD,
                        ),
                        ft.Text(
                            filter_item["label"],
                            size=11,
                            weight=ft.FontWeight.W_700,
                            color=COLOR_GOOD,
                        ),
                    ],
                    spacing=6,
                ),
                bgcolor="#132a28",
                border=ft.Border.all(1.2, COLOR_GOOD),
                border_radius=ft.BorderRadius.all(20),
                padding=ft.Padding.symmetric(horizontal=12, vertical=6),
                on_click=on_click,
                ink=True,
            )
        else:
            return ft.Container(
                content=ft.Text(
                    filter_item["label"],
                    size=11,
                    weight=ft.FontWeight.W_500,
                    color=TEXT_MUTED,
                ),
                bgcolor="#141b24",
                border=ft.Border.all(1, BORDER_COLOR),
                border_radius=ft.BorderRadius.all(20),
                padding=ft.Padding.symmetric(horizontal=12, vertical=6),
                on_click=on_click,
                ink=True,
            )

    def _safe_update(self):
        """Atualiza a página de forma segura quando anexada à árvore de controles."""
        try:
            self.update()
        except Exception:
            pass

    def _refresh_filters(self):
        """Atualiza visualmente as pills de filtro."""
        self.filter_row.controls = [
            self._build_filter_pill(f) for f in self.filters
        ]
        self._safe_update()

    def _build_top_control_bar(self) -> ft.Container:
        """Barra superior enxuta com dados da fazenda, seletor de camadas e botões de ação."""
        farm_header = ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Icon(
                            icon=ft.Icons.LOCATION_ON_ROUNDED,
                            size=18,
                            color=COLOR_EXCELLENT,
                        ),
                        ft.Text(
                            FARM_INFO["name"],
                            size=15,
                            weight=ft.FontWeight.BOLD,
                            color=TEXT_WHITE,
                        ),
                        ft.Container(
                            content=ft.Text(
                                FARM_INFO["season"],
                                size=10.5,
                                weight=ft.FontWeight.W_600,
                                color="#00d2b4",
                            ),
                            bgcolor="#0d2b22",
                            padding=ft.Padding.symmetric(horizontal=8, vertical=3),
                            border_radius=ft.BorderRadius.all(6),
                            border=ft.Border.all(1, "#144d37"),
                        ),
                    ],
                    spacing=8,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Text(
                    f"{FARM_INFO['total_area']} • {FARM_INFO['total_talhoes']} Talhões • {FARM_INFO['municipality']}",
                    size=11,
                    color=TEXT_MUTED,
                ),
            ],
            spacing=2,
        )

        # Botões de Ação
        actions = ft.Row(
            controls=[
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Icon(icon=ft.Icons.STRAIGHTEN_ROUNDED, size=13, color="#cbd5e1"),
                            ft.Text("Medir Área", size=11, weight=ft.FontWeight.W_600, color="#cbd5e1"),
                        ],
                        spacing=5,
                    ),
                    bgcolor="#141b24",
                    border=ft.Border.all(1, BORDER_COLOR),
                    border_radius=ft.BorderRadius.all(8),
                    padding=ft.Padding.symmetric(horizontal=10, vertical=6),
                    ink=True,
                ),
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Icon(icon=ft.Icons.FILE_DOWNLOAD_OUTLINED, size=13, color="#cbd5e1"),
                            ft.Text("Exportar KML", size=11, weight=ft.FontWeight.W_600, color="#cbd5e1"),
                        ],
                        spacing=5,
                    ),
                    bgcolor="#141b24",
                    border=ft.Border.all(1, BORDER_COLOR),
                    border_radius=ft.BorderRadius.all(8),
                    padding=ft.Padding.symmetric(horizontal=10, vertical=6),
                    ink=True,
                ),
                ft.Container(
                    content=ft.Row(
                        controls=[
                            ft.Icon(icon=ft.Icons.ADD_ROUNDED, size=14, color="#0b0f14"),
                            ft.Text("Novo Talhão", size=11, weight=ft.FontWeight.BOLD, color="#0b0f14"),
                        ],
                        spacing=4,
                    ),
                    bgcolor=COLOR_GOOD,
                    border_radius=ft.BorderRadius.all(8),
                    padding=ft.Padding.symmetric(horizontal=12, vertical=6),
                    ink=True,
                ),
            ],
            spacing=8,
        )

        # Linha de filtros
        self.filter_row = ft.Row(
            controls=[self._build_filter_pill(f) for f in self.filters],
            spacing=8,
            wrap=True,
        )

        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            farm_header,
                            actions,
                        ],
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        vertical_alignment=ft.CrossAxisAlignment.CENTER,
                    ),
                    ft.Container(height=2),
                    self.filter_row,
                ],
                spacing=6,
            ),
            bgcolor=BG_CARD,
            border=ft.Border.all(1, BORDER_COLOR),
            border_radius=ft.BorderRadius.all(16),
            padding=ft.Padding.all(14),
        )

    def _toggle_map_expand(self):
        """Alterna entre o modo de visualização padrão e ampliado do mapa."""
        self.is_map_expanded = not self.is_map_expanded

        # Atualiza a visibilidade do painel lateral e a altura do mapa
        self.detail_container.visible = not self.is_map_expanded
        self.map_container.height = 540 if self.is_map_expanded else 430

        # Atualiza o mapa com o novo estado de expansão
        self.map_container.content = MapFullView(
            on_talhao_click=self._on_talhao_selected,
            selected_talhao_id=self.selected_talhao_id,
            on_toggle_expand=self._toggle_map_expand,
            is_expanded=self.is_map_expanded,
        )

        self._safe_update()

    def _on_talhao_selected(self, talhao_id: str):
        """Callback executado ao clicar em um talhão no mapa ou na tabela."""
        self.selected_talhao_id = talhao_id

        # Atualiza o detalhe do talhão
        self.detail_container.content = TalhaoDetailCard(talhao_id=talhao_id)

        # Atualiza o mapa com o talhão selecionado em destaque
        self.map_container.content = MapFullView(
            on_talhao_click=self._on_talhao_selected,
            selected_talhao_id=talhao_id,
            on_toggle_expand=self._toggle_map_expand,
            is_expanded=self.is_map_expanded,
        )

        self._safe_update()


