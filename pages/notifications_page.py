"""Detailed alerts and recommendations related to the current plots."""
import flet as ft

from theme import (BG_MAIN, TEXT_WHITE, TEXT_MUTED, COLOR_GOOD,
                   COLOR_WARNING, COLOR_CRITICAL, COLOR_BLUE, BORDER_COLOR)
from telemetry import get_notifications, get_devices
from pages.page_ui import heading, panel, label, device_dropdown


class NotificationsPage(ft.Container):
    def __init__(self, **kwargs):
        self.items = get_notifications()
        self.devices = get_devices()
        self.category = "Todas"
        self.device_id = "all"
        self.list_column = ft.Column(spacing=10)
        self.count_text = label("")
        self.device_dropdown = device_dropdown(self.devices, "all", self._device_changed,
                                               include_all=True, width=320)
        self.category_dropdown = ft.Dropdown(
            value="Todas", options=[ft.DropdownOption(key=x, text=x)
                                     for x in ("Todas", "Alerta", "Indicação")],
            width=180, dense=True, label="Tipo", border_color=BORDER_COLOR,
            focused_border_color=COLOR_GOOD, on_select=self._category_changed)
        content = ft.Column([
            heading("Notificações", "Alertas e indicações dos talhões monitorados",
                    ft.Icons.NOTIFICATIONS_NONE_ROUNDED),
            ft.ResponsiveRow([
                self._stat("Alertas", sum(n["category"] == "Alerta" for n in self.items),
                           ft.Icons.WARNING_AMBER_ROUNDED, COLOR_WARNING),
                self._stat("Indicações", sum(n["category"] == "Indicação" for n in self.items),
                           ft.Icons.LIGHTBULB_OUTLINE_ROUNDED, COLOR_GOOD),
                self._stat("Dispositivos offline", sum(not d["online"] for d in self.devices),
                           ft.Icons.SENSORS_OFF_ROUNDED, COLOR_CRITICAL),
            ], spacing=14, run_spacing=14),
            panel(ft.Column([
                ft.Row([ft.Text("Central de notificações", color=TEXT_WHITE, size=17,
                                weight=ft.FontWeight.BOLD), self.count_text],
                       alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                ft.Row([self.category_dropdown, self.device_dropdown], spacing=12, wrap=True),
                label("Avisos derivados dos dados de demonstração; não são eventos em tempo real.", COLOR_BLUE),
                self.list_column,
            ], spacing=14)),
        ], spacing=18, scroll=ft.ScrollMode.AUTO, expand=True)
        super().__init__(content=content, padding=20, bgcolor=BG_MAIN, expand=True, **kwargs)
        self._render()

    def _stat(self, title, value, icon, color):
        return panel(ft.Row([
            ft.Container(ft.Icon(icon, color=color, size=25), width=46, height=46,
                         bgcolor="#101720", border_radius=10, alignment=ft.Alignment.CENTER),
            ft.Column([label(title.upper()), ft.Text(str(value), color=TEXT_WHITE,
                                                      size=24, weight=ft.FontWeight.BOLD)], spacing=3),
        ], spacing=12), col={"sm": 12, "md": 4})

    def _category_changed(self, e):
        self.category = e.control.value
        self._render()
        self.update()

    def _device_changed(self, e):
        self.device_id = e.control.value
        self._render()
        self.update()

    def _render(self):
        visible = [n for n in self.items if
                   (self.category == "Todas" or n["category"] == self.category) and
                   (self.device_id == "all" or n["device_id"] == self.device_id)]
        self.count_text.value = f"{len(visible)} resultado(s)"
        self.list_column.controls = [self._notice(n) for n in visible] or [
            ft.Container(ft.Text("Nenhuma notificação para estes filtros.", color=TEXT_MUTED),
                         padding=25, alignment=ft.Alignment.CENTER)]

    def _notice(self, notice):
        is_alert = notice["category"] == "Alerta"
        color = (COLOR_CRITICAL if notice["severity"] == "Crítico" else COLOR_WARNING) if is_alert else COLOR_GOOD
        icon = ft.Icons.WARNING_AMBER_ROUNDED if is_alert else ft.Icons.LIGHTBULB_OUTLINE_ROUNDED
        return ft.Container(
            content=ft.Row([
                ft.Container(ft.Icon(icon, color=color, size=23), width=46, height=46,
                             bgcolor="#101720", border_radius=10, alignment=ft.Alignment.CENTER),
                ft.Column([
                    ft.Row([ft.Text(notice["title"], color=TEXT_WHITE, size=13,
                                    weight=ft.FontWeight.BOLD, expand=True),
                            label(notice["severity"], color)], spacing=10),
                    ft.Text(notice["description"], color="#b5c4d1", size=12),
                    label(f'{notice["location"]} · {notice["source"]} · {notice["category"]}'),
                ], spacing=5, expand=True),
            ], spacing=13, vertical_alignment=ft.CrossAxisAlignment.START),
            padding=16, bgcolor="#101720", border=ft.Border.all(1, BORDER_COLOR), border_radius=11,
        )
