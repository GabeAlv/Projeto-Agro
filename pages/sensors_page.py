"""IoT telemetry by plot, using the same demo snapshot as the other pages."""
import flet as ft

from theme import (BG_MAIN, BORDER_COLOR, TEXT_WHITE, TEXT_MUTED,
                   COLOR_GOOD, COLOR_WARNING, COLOR_CRITICAL, COLOR_BLUE)
from telemetry import METRICS, get_devices, format_value
from pages.page_ui import heading, panel, label, device_dropdown
from components.sensor_chart_card import create_sparkline_canvas


METRIC_STYLE = {
    "air_temp": (ft.Icons.DEVICE_THERMOSTAT_ROUNDED, COLOR_WARNING, "Temperatura do ar"),
    "soil_humidity": (ft.Icons.WATER_DROP_ROUNDED, COLOR_GOOD, "Umidade do solo"),
    "air_humidity": (ft.Icons.WATER_DROP_OUTLINED, COLOR_BLUE, "Umidade do ar"),
}


class SensorsPage(ft.Container):
    def __init__(self, **kwargs):
        self.devices = get_devices()
        self.selected_id = self.devices[0]["id"]
        self.summary = ft.ResponsiveRow(spacing=14, run_spacing=14)
        self.detail = ft.Container()
        self.dropdown = device_dropdown(self.devices, self.selected_id, self._select)
        content = ft.Column([
            ft.Row([
                heading("Sensores IoT", "Telemetria por talhão e dispositivo", ft.Icons.MEMORY_ROUNDED),
                self.dropdown,
            ], alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
               vertical_alignment=ft.CrossAxisAlignment.CENTER, wrap=True),
            ft.Container(
                content=ft.Row([
                    ft.Icon(ft.Icons.INFO_OUTLINE, color=COLOR_BLUE, size=18),
                    ft.Text("Dados de demonstração · cada talhão corresponde a um dispositivo IoT. Leituras sem conexão ficam indisponíveis.",
                            color="#a8bacb", size=12, expand=True),
                ], spacing=10),
                padding=ft.Padding.symmetric(horizontal=16, vertical=12),
                bgcolor="#10202d", border=ft.Border.all(1, "#214057"), border_radius=10,
            ),
            self.summary,
            self.detail,
            panel(ft.Column([
                ft.Text("Dispositivos da fazenda", color=TEXT_WHITE, size=17, weight=ft.FontWeight.BOLD),
                label("Selecione um dispositivo para consultar suas leituras e o histórico ilustrativo."),
                ft.ResponsiveRow([self._device_row(d) for d in self.devices], spacing=10, run_spacing=10),
            ], spacing=12)),
        ], spacing=18, scroll=ft.ScrollMode.AUTO, expand=True)
        super().__init__(content=content, padding=20, bgcolor=BG_MAIN, expand=True, **kwargs)
        self._render()

    def _select(self, e):
        self.selected_id = e.control.value
        self._render()
        self.update()

    def _choose(self, device_id):
        self.selected_id = device_id
        self.dropdown.value = device_id
        self._render()
        self.update()

    def _metric_card(self, device, metric_id, title, unit):
        icon, color, _ = METRIC_STYLE[metric_id]
        value = device["values"][metric_id]
        history = device["history"][metric_id]
        value_text = format_value(value, unit)
        minimum = f"{min(history):g}{unit}" if history else "—"
        maximum = f"{max(history):g}{unit}" if history else "—"
        chart = create_sparkline_canvas(history, color, width=300, height=64) if history else ft.Container(
            ft.Text("Aguardando conexão para exibir o histórico", color=TEXT_MUTED, size=11), height=64,
            alignment=ft.Alignment.CENTER_LEFT)
        return panel(ft.Column([
            ft.Row([ft.Icon(icon, color=color, size=22), label(title.upper(), "#cbd5e1", 12)], spacing=8),
            ft.Text(value_text, color=TEXT_WHITE if value is not None else TEXT_MUTED,
                    size=31 if value is not None else 21, weight=ft.FontWeight.BOLD),
            label("Última leitura de demonstração" if value is not None else "Dispositivo offline"),
            ft.Container(chart, padding=ft.Padding.symmetric(vertical=8)),
            ft.Row([label(f"Mín. {minimum}"), label(f"Máx. {maximum}")],
                   alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
            label("13 pontos ilustrativos · janela de 24h" if history else "Sem histórico disponível"),
        ], spacing=9), col={"sm": 12, "md": 6, "lg": 4})

    def _device_row(self, device):
        active = device["id"] == self.selected_id
        status_color = COLOR_GOOD if device["online"] else COLOR_CRITICAL
        return ft.Container(
            content=ft.Row([
                ft.Icon(ft.Icons.SENSORS_ROUNDED, color=status_color, size=19),
                ft.Column([
                    ft.Text(device["name"], color=TEXT_WHITE, size=12, weight=ft.FontWeight.BOLD),
                    label((device["nickname"] or device["device_id"]) + " · " + ("Online" if device["online"] else "Offline"), status_color, 10),
                ], spacing=2, expand=True),
                ft.Icon(ft.Icons.CHEVRON_RIGHT_ROUNDED, color=TEXT_MUTED, size=18),
            ], spacing=10),
            col={"sm": 12, "md": 6, "lg": 3}, padding=12, bgcolor="#132a28" if active else "#101720",
            border=ft.Border.all(1, COLOR_GOOD if active else BORDER_COLOR), border_radius=10,
            on_click=lambda e, device_id=device["id"]: self._choose(device_id), ink=True,
        )

    def _render(self):
        device = next(d for d in self.devices if d["id"] == self.selected_id)
        self.summary.controls = [self._metric_card(device, *metric) for metric in METRICS]
        status_color = COLOR_GOOD if device["online"] else COLOR_CRITICAL
        self.detail.content = panel(ft.ResponsiveRow([
            ft.Column([
                label("DISPOSITIVO SELECIONADO"),
                ft.Text(device["device_id"], color=TEXT_WHITE, size=19, weight=ft.FontWeight.BOLD),
                label(device["nickname"], COLOR_GOOD) if device["nickname"] else ft.Container(),
                label(f'{device["name"]} · {device["crop"]} · {device["area"]}'),
            ], spacing=6, col={"sm": 12, "md": 6}),
            ft.Column([
                label("CONDIÇÃO DO TALHÃO"),
                ft.Text(device["status"], color=status_color, size=17, weight=ft.FontWeight.BOLD),
                label("Conectado" if device["online"] else "Sem comunicação; leituras indisponíveis"),
            ], spacing=6, col={"sm": 12, "md": 6}),
        ], spacing=12))
        # Rebuild the selector cards to reflect the active device.
        device_panel = self.content.controls[-1]
        device_panel.content.controls[-1].controls = [self._device_row(d) for d in self.devices]
