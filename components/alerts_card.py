"""
Componente de Notificações e Alertas Preditivos de IA/ML.
Herdando de BaseCard.
"""
import flet as ft
from theme import (
    TEXT_WHITE,
    TEXT_MUTED,
    CRITICAL_TAG_BG,
    CRITICAL_TAG_TEXT,
)
from mock_data import NOTIFICATIONS_DATA
from components.base_card import BaseCard


def create_notification_item(item: dict) -> ft.Container:
    """Cria uma linha de notificação estilizada."""
    return ft.Container(
        content=ft.Row(
            controls=[
                # Ícone em quadrado com fundo correspondente
                ft.Container(
                    content=ft.Icon(
                        icon=item["icon"],
                        size=20,
                        color=item["color"],
                    ),
                    width=38,
                    height=38,
                    border_radius=ft.BorderRadius.all(10),
                    bgcolor=item["bg_color"],
                    alignment=ft.Alignment.CENTER,
                ),
                # Título e Talhão
                ft.Column(
                    controls=[
                        ft.Text(
                            item["title"],
                            size=12,
                            weight=ft.FontWeight.W_700,
                            color=TEXT_WHITE,
                        ),
                        ft.Text(
                            item["location"],
                            size=11,
                            color=TEXT_MUTED,
                        ),
                    ],
                    spacing=2,
                    expand=True,
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
                # Tag de origem do modelo
                ft.Text(
                    item["source_tag"],
                    size=10,
                    color=TEXT_MUTED,
                    weight=ft.FontWeight.W_500,
                ),
            ],
            spacing=12,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        bgcolor="#111720",
        border_radius=ft.BorderRadius.all(12),
        padding=ft.Padding.symmetric(horizontal=12, vertical=10),
        border=ft.Border.all(1, "#1e293b"),
    )


class AlertsCard(BaseCard):
    """Card de Notificações e Alertas herdando de BaseCard."""
    def __init__(self, data: dict = NOTIFICATIONS_DATA, **kwargs):
        # Cabeçalho com badge "Crítico"
        header = ft.Row(
            controls=[
                ft.Text(
                    data["title"],
                    size=13,
                    weight=ft.FontWeight.W_800,
                    color="#cbd5e1",
                ),
                ft.Container(
                    content=ft.Text(
                        data["badge_text"],
                        size=10.5,
                        weight=ft.FontWeight.BOLD,
                        color=CRITICAL_TAG_TEXT,
                    ),
                    bgcolor=CRITICAL_TAG_BG,
                    padding=ft.Padding.symmetric(horizontal=8, vertical=3),
                    border_radius=ft.BorderRadius.all(6),
                    border=ft.Border.all(1, "#5f1d24"),
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        items_list = [create_notification_item(item) for item in data["items"]]

        content = ft.Column(
            controls=[
                header,
                ft.Container(height=4),
                *items_list,
            ],
            spacing=10,
        )

        super().__init__(
            content=content,
            **kwargs,
        )


def create_alerts_card(data: dict = NOTIFICATIONS_DATA) -> AlertsCard:
    """Factory helper para instanciar o AlertsCard."""
    return AlertsCard(data=data)
