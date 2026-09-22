"""
Ponto de entrada do Frontend da Aplicação IMK em Flet.
Gerencia roteamento e troca dinâmica entre Dashboard e Página do Mapa.
"""
import flet as ft
from theme import BG_MAIN
from components.sidebar import create_sidebar
from components.header import create_header
from pages.dashboard_page import DashboardPage
from pages.map_page import MapPage


def main(page: ft.Page):
    # Configurações globais da página
    page.title = "IMK - Monitoramento Agrícola & Sensoriamento Espacial"
    page.bgcolor = BG_MAIN
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = ft.Padding.all(0)
    page.spacing = 0

    # Estado de rota atual
    current_route = "dashboard"

    # Cabeçalho Superior Fixo
    header = create_header()

    # Container da Barra Lateral (para permitir re-renderizar estado ativo)
    sidebar_container = ft.Container()

    # Container de Conteúdo Dinâmico (onde a página atual é renderizada)
    content_area = ft.Container(expand=True)

    def navigate_to(route_name: str):
        nonlocal current_route
        current_route = route_name

        # Atualiza a sidebar com a rota ativa correta
        sidebar_container.content = create_sidebar(
            active_route=current_route,
            on_navigate=navigate_to,
        )

        # Atualiza o conteúdo conforme a rota selecionada
        if current_route == "map":
            content_area.content = MapPage()
        else:
            # Padrão: dashboard
            content_area.content = DashboardPage(on_navigate=navigate_to)

        page.update()

    # Inicializa Sidebar e Página inicial
    sidebar_container.content = create_sidebar(
        active_route=current_route,
        on_navigate=navigate_to,
    )
    content_area.content = DashboardPage(on_navigate=navigate_to)

    # Layout Principal: Sidebar + Conteúdo
    body = ft.Row(
        controls=[
            sidebar_container,
            content_area,
        ],
        spacing=0,
        expand=True,
        vertical_alignment=ft.CrossAxisAlignment.STRETCH,
    )

    # Adiciona a estrutura completa à página
    page.add(
        ft.Column(
            controls=[
                header,
                ft.Container(
                    content=body,
                    expand=True,
                ),
            ],
            spacing=0,
            expand=True,
        )
    )


if __name__ == "__main__":
    ft.app(target=main)
