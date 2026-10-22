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
    COLOR_GOOD,
    COLOR_WARNING,
)
from telemetry import get_notifications
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
    def __init__(self, data: dict = None, **kwargs):
        badge_color = CRITICAL_TAG_TEXT
        badge_background = CRITICAL_TAG_BG
        if data is None:
            notices = [n for n in get_notifications() if n["category"] == "Alerta"]
            notices.sort(key=lambda n: n["severity"] != "Crítico")
            critical = any(n["severity"] == "Crítico" for n in notices)
            badge_color = CRITICAL_TAG_TEXT if critical else COLOR_WARNING if notices else COLOR_GOOD
            badge_background = CRITICAL_TAG_BG if critical else "#332710" if notices else "#10312b"
            data = {
                "title": "ALERTAS DOS TALHÕES",
                "badge_text": f"{len(notices)} ativo(s)" if notices else "Sem alertas",
                "items": [{
                    "title": notice["title"], "location": notice["location"],
                    "source_tag": "Regra · demo",
                    "icon": ft.Icons.WARNING_AMBER_ROUNDED,
                    "color": CRITICAL_TAG_TEXT if notice["severity"] == "Crítico" else COLOR_WARNING,
                    "bg_color": CRITICAL_TAG_BG if notice["severity"] == "Crítico" else "#332710",
                } for notice in notices[:3]],
            }
            remaining = max(0, len(notices) - 3)
        else:
            remaining = 0
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
                        color=badge_color,
                    ),
                    bgcolor=badge_background,
                    padding=ft.Padding.symmetric(horizontal=8, vertical=3),
                    border_radius=ft.BorderRadius.all(6),
                    border=ft.Border.all(1, badge_color),
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        items_list = [create_notification_item(item) for item in data["items"]]
        if not items_list:
            items_list = [ft.Text("Nenhum alerta ativo com as regras atuais.", color=TEXT_MUTED, size=12)]
        if remaining:
            items_list.append(ft.Text(f"Mais {remaining} alerta(s) na página de Notificações.",
                                      color=TEXT_MUTED, size=11))

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


def create_alerts_card(data: dict = None) -> AlertsCard:
    """Factory helper para instanciar o AlertsCard."""
    return AlertsCard(data=data)
