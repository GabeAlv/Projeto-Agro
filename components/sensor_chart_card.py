"""
Componente de Card de Métrica de Sensor com Gráfico Histórico 24h.
Herdando de BaseCard.
"""
import flet as ft
import flet.canvas as cv
from theme import (
    TEXT_WHITE,
    TEXT_SECONDARY,
    TEXT_MUTED,
)
from components.base_card import BaseCard


def create_sparkline_canvas(data: list[float], color_hex: str, width: float = 175, height: float = 48) -> ft.Control:
    """Desenha a linha do gráfico histórico de 24h com base nos pontos fornecidos."""
    if not data:
        return ft.Container(height=height)

    min_val = min(data)
    max_val = max(data)
    val_range = max_val - min_val if max_val != min_val else 1.0

    padding_y = 6
    usable_h = height - (2 * padding_y)
    usable_w = width

    step_x = usable_w / (len(data) - 1)

    points = []
    for i, val in enumerate(data):
        x = i * step_x
        norm_y = (val - min_val) / val_range
        y = height - padding_y - (norm_y * usable_h)
        points.append((x, y))

    # Constrói o Path
    path_elements = [cv.Path.MoveTo(points[0][0], points[0][1])]
    for x, y in points[1:]:
        path_elements.append(cv.Path.LineTo(x, y))

    stroke_paint = ft.Paint(
        color=color_hex,
        stroke_width=2.2,
        style=ft.PaintingStyle.STROKE,
        stroke_cap=ft.StrokeCap.ROUND,
        stroke_join=ft.StrokeJoin.ROUND,
    )

    path_shape = cv.Path(
        path_elements,
        paint=stroke_paint,
    )

    return cv.Canvas(
        shapes=[path_shape],
        width=usable_w,
        height=height,
    )


class SensorChartCard(BaseCard):
    """Card de Métrica de Sensor com gráfico 24h herdando de BaseCard."""
    def __init__(self, sensor: dict, expand: bool | int = True, padding: ft.Padding | None = None, **kwargs):
        # Topo do Card
        header = ft.Row(
            controls=[
                ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Icon(
                                icon=sensor["icon"],
                                size=18,
                                color=sensor["icon_color"],
                            ),
                            width=32,
                            height=32,
                            border_radius=ft.BorderRadius.all(8),
                            bgcolor="#121820",
                            alignment=ft.Alignment.CENTER,
                        ),
                        ft.Text(
                            sensor["title"],
                            size=11,
                            weight=ft.FontWeight.W_800,
                            color="#cbd5e1",
                        ),
                    ],
                    spacing=8,
                    vertical_alignment=ft.CrossAxisAlignment.CENTER,
                ),
                ft.Text(
                    sensor["reading_label"],
                    size=10,
                    color=TEXT_MUTED,
                ),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        # Valor Principal e Badge de Tendência
        trend_icon = ft.Icons.TRENDING_UP_ROUNDED if sensor["trend_type"] == "up" else ft.Icons.TRENDING_DOWN_ROUNDED
        trend_badge = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(
                        icon=trend_icon,
                        size=14,
                        color=sensor["chart_color"],
                    ),
                    ft.Text(
                        sensor["trend_val"],
                        size=11,
                        weight=ft.FontWeight.BOLD,
                        color=sensor["chart_color"],
                    ),
                ],
                spacing=3,
            ),
            bgcolor="#111822",
            padding=ft.Padding.symmetric(horizontal=6, vertical=2),
            border_radius=ft.BorderRadius.all(6),
            border=ft.Border.all(1, "#1e293b"),
        )

        val_row = ft.Row(
            controls=[
                ft.Row(
                    controls=[
                        ft.Text(
                            sensor["value"],
                            size=28,
                            weight=ft.FontWeight.W_900,
                            color=TEXT_WHITE,
                        ),
                        ft.Container(
                            content=ft.Text(
                                sensor["unit"],
                                size=12,
                                weight=ft.FontWeight.BOLD,
                                color=TEXT_SECONDARY,
                            ),
                            padding=ft.Padding.only(bottom=4),
                            alignment=ft.Alignment.BOTTOM_LEFT,
                        ),
                    ],
                    spacing=4,
                    vertical_alignment=ft.CrossAxisAlignment.END,
                ),
                trend_badge,
            ],
            spacing=12,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        # Gráfico + Rótulos de Máx / Mín
        chart_canvas = create_sparkline_canvas(
            data=sensor["history"],
            color_hex=sensor["chart_color"],
            width=175,
            height=48,
        )

        y_axis_labels = ft.Column(
            controls=[
                ft.Text(sensor["max_label"], size=9.5, color=TEXT_MUTED),
                ft.Text(sensor["min_label"], size=9.5, color=TEXT_MUTED),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            horizontal_alignment=ft.CrossAxisAlignment.END,
            height=48,
        )

        chart_section = ft.Row(
            controls=[
                chart_canvas,
                y_axis_labels,
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            vertical_alignment=ft.CrossAxisAlignment.CENTER,
        )

        # Eixo de tempo inferior (6h, 12h, 24h)
        time_row = ft.Row(
            controls=[
                ft.Text("6h", size=9.5, color=TEXT_MUTED),
                ft.Text("12h", size=9.5, color=TEXT_MUTED),
                ft.Text("24h", size=9.5, color=TEXT_MUTED),
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

        content = ft.Column(
            controls=[
                header,
                val_row,
                chart_section,
                time_row,
            ],
            spacing=8,
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        )

        super().__init__(
            content=content,
            padding=padding or ft.Padding.all(16),
            expand=expand,
            **kwargs,
        )


def create_sensor_card(sensor: dict) -> SensorChartCard:
    """Factory helper para instanciar o SensorChartCard."""
    return SensorChartCard(sensor=sensor)
