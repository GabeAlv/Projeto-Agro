"""Shared layout primitives for the new sections."""
import flet as ft
from theme import BG_CARD, BORDER_COLOR, TEXT_WHITE, TEXT_MUTED, COLOR_GOOD


def heading(title, subtitle, icon):
    return ft.Row([
        ft.Container(ft.Icon(icon, color=COLOR_GOOD, size=24), width=48, height=48,
                     bgcolor="#10312d", border_radius=12, alignment=ft.Alignment.CENTER),
        ft.Column([
            ft.Text(title, size=25, weight=ft.FontWeight.BOLD, color=TEXT_WHITE),
            ft.Text(subtitle, size=12, color=TEXT_MUTED),
        ], spacing=2),
    ], spacing=14, vertical_alignment=ft.CrossAxisAlignment.CENTER)


def panel(content, col=12, padding=20):
    return ft.Container(content=content, col=col, padding=padding, bgcolor=BG_CARD,
                        border=ft.Border.all(1, BORDER_COLOR), border_radius=16)


def label(text, color=TEXT_MUTED, size=11):
    return ft.Text(text, size=size, color=color, weight=ft.FontWeight.W_600)


def device_dropdown(devices, value, on_select, include_all=False, width=280):
    options = [ft.DropdownOption(key="all", text="Todos os dispositivos")] if include_all else []
    options += [ft.DropdownOption(key=d["id"], text=f'{d.get("nickname") or d["device_id"]} · {d["name"]}') for d in devices]
    return ft.Dropdown(value=value, options=options, width=width, dense=True,
                       label="Dispositivo IoT", border_color=BORDER_COLOR,
                       focused_border_color=COLOR_GOOD, on_select=on_select)
