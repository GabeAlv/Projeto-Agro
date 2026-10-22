"""
Ponto de entrada do Frontend da Aplicação STS em Flet.
 Gerencia roteamento e troca dinâmica entre as seções do dashboard.
"""
import flet as ft
from theme import BG_MAIN
from components.sidebar import create_sidebar
from components.header import create_header
from pages.dashboard_page import DashboardPage
from pages.map_page import MapPage
from pages.sensors_page import SensorsPage
from pages.reports_page import ReportsPage
from pages.notifications_page import NotificationsPage
from pages.settings_page import SettingsPage
from settings_store import load_settings, ROUTES

def main(page: ft.Page):
    # Configurações globais da página
    page.title = "STS - Monitoramento Agrícola & Sensoriamento Espacial"
    page.bgcolor = BG_MAIN
    page.theme_mode = ft.ThemeMode.DARK
    page.padding = ft.Padding.all(0)
    page.spacing = 0

    # Estado de rota atual
    current_route = load_settings()["preferences"]["initial_route"]

    # Cabeçalho Superior Fixo
    header = ft.Container(content=create_header())

    def settings_saved(settings):
        header.content = create_header(settings)
        page.title = f'STS - {settings["property"]["name"]}'
        page.update()

    settings_page = SettingsPage(on_saved=settings_saved)

    # Container da Barra Lateral (para permitir re-renderizar estado ativo)
    sidebar_container = ft.Container()

    # Container de Conteúdo Dinâmico (onde a página atual é renderizada)
    content_area = ft.Container(expand=True)

    def navigate_to(route_name: str):
        nonlocal current_route
        current_route = route_name if route_name in ROUTES else "dashboard"

        # Atualiza a sidebar com a rota ativa correta
        sidebar_container.content = create_sidebar(
            active_route=current_route,
            on_navigate=navigate_to,
        )

        # Atualiza o conteúdo conforme a rota selecionada
        if current_route == "map":
            content_area.content = MapPage()
        elif current_route == "sensors":
            content_area.content = SensorsPage()
        elif current_route == "reports":
            content_area.content = ReportsPage()
        elif current_route == "notifications":
            content_area.content = NotificationsPage()
        elif current_route == "settings":
            content_area.content = settings_page
        else:
            # Padrão: dashboard
            content_area.content = DashboardPage(on_navigate=navigate_to)

        page.update()

    # Usa a mesma navegação na abertura para respeitar a página inicial salva.
    navigate_to(current_route)

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
