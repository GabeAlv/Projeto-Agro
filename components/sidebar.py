"""
Componente de Barra Lateral (Sidebar) com navegação de ícones.
Suporta callback de navegação entre páginas.
"""
import flet as ft
from theme import (
    BG_SIDEBAR,
    TEXT_MUTED,
    COLOR_GOOD,
    BORDER_COLOR,
)


def create_nav_item(icon_data, is_active: bool = False, tooltip: str = "", on_click=None):
    """Cria um botão de navegação para a sidebar com estado ativo/inativo estilizado."""
    if is_active:
        return ft.Container(
            content=ft.Icon(
                icon=icon_data,
                size=22,
                color=COLOR_GOOD,
            ),
            width=48,
            height=48,
            border_radius=ft.BorderRadius.all(12),
            border=ft.Border.all(1.5, COLOR_GOOD),
            bgcolor="#132a28",
            alignment=ft.Alignment.CENTER,
            tooltip=tooltip,
            on_click=on_click,
            ink=True,
        )
    else:
        return ft.Container(
            content=ft.Icon(
                icon=icon_data,
                size=22,
                color=TEXT_MUTED,
            ),
            width=48,
            height=48,
            border_radius=ft.BorderRadius.all(12),
            alignment=ft.Alignment.CENTER,
            tooltip=tooltip,
            ink=True,
            on_click=on_click,
        )


def create_sidebar(active_route: str = "dashboard", on_navigate=None) -> ft.Container:
    """Retorna o container da barra lateral estilizada com suporte a rotas dinâmicas."""

    def make_nav_handler(route_name: str):
        def handler(e):
            if on_navigate:
                on_navigate(route_name)
        return handler

    nav_items = [
        (ft.Icons.GRID_VIEW_ROUNDED, "dashboard", "Dashboard Geral"),
        (ft.Icons.MAP_OUTLINED, "map", "Mapa de Talhões"),
        (ft.Icons.MEMORY_ROUNDED, "sensors", "Sensores IoT & Telemetria"),
        (ft.Icons.DESCRIPTION_OUTLINED, "reports", "Relatórios & Laudos"),
        (ft.Icons.NOTIFICATIONS_NONE_ROUNDED, "notifications", "Notificações"),
        (ft.Icons.SETTINGS_OUTLINED, "settings", "Configurações"),
    ]

    nav_controls = []
    for icon, route, tip in nav_items:
        is_active = route == active_route
        nav_controls.append(
            create_nav_item(
                icon_data=icon,
                is_active=is_active,
                tooltip=tip,
                on_click=make_nav_handler(route),
            )
        )

    nav_icons = ft.Column(
        controls=nav_controls,
        spacing=16,
        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
    )

    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Container(height=16),
                nav_icons,
                ft.Container(expand=True),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        width=72,
        bgcolor=BG_SIDEBAR,
        border=ft.Border.only(right=ft.BorderSide(1, BORDER_COLOR)),
        padding=ft.Padding.symmetric(vertical=8),
        alignment=ft.Alignment.CENTER,
    )
