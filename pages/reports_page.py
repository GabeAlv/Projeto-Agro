"""Report preview and PDF download for the current demo snapshot."""
from datetime import datetime
import flet as ft

from theme import BG_MAIN, TEXT_WHITE, TEXT_MUTED, COLOR_GOOD, COLOR_BLUE, COLOR_WARNING
from telemetry import METRICS, get_devices, get_notifications, format_value
from pages.page_ui import heading, panel, label, device_dropdown
from report_pdf import create_report_pdf


class ReportsPage(ft.Container):
    def __init__(self, **kwargs):
        self.devices = get_devices()
        self.notifications = get_notifications()
        self.selected_id = "all"
        self.snapshot = None
        self.picker = ft.FilePicker()
        self.preview = ft.Column(spacing=12)
        self.download_button = ft.Button("Baixar PDF", icon=ft.Icons.PICTURE_AS_PDF_ROUNDED,
                                         bgcolor="#0e5f50", color=TEXT_WHITE,
                                         disabled=True, on_click=self._download)
        self.dropdown = device_dropdown(self.devices, "all", self._select, include_all=True, width=340)
        content = ft.Column([
            heading("Relatórios", "Gere um resumo a partir dos dados atuais do dashboard", ft.Icons.DESCRIPTION_OUTLINED),
            panel(ft.Column([
                ft.Text("Configurar relatório", color=TEXT_WHITE, size=17, weight=ft.FontWeight.BOLD),
                label("Escolha os talhões incluídos. A prévia captura as leituras e notificações exibidas no momento da geração."),
                ft.Row([self.dropdown,
                        ft.Button("Gerar relatório", icon=ft.Icons.AUTO_AWESOME_ROUNDED,
                                  bgcolor=COLOR_GOOD, color="#06231f", on_click=self._generate),
                        self.download_button], spacing=12, wrap=True),
                label("Fonte: dados de demonstração · formato PDF A4 · leituras sem conexão aparecem como indisponíveis.",
                      COLOR_BLUE),
            ], spacing=16)),
            panel(ft.Column([
                ft.Row([ft.Text("Prévia do relatório", color=TEXT_WHITE, size=17,
                                weight=ft.FontWeight.BOLD),
                        ft.Icon(ft.Icons.PREVIEW_ROUNDED, color=COLOR_GOOD)],
                       alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                self.preview,
            ], spacing=14)),
        ], spacing=18, scroll=ft.ScrollMode.AUTO, expand=True)
        super().__init__(content=content, padding=20, bgcolor=BG_MAIN, expand=True, **kwargs)
        self._render_preview()

    def did_mount(self):
        if self.picker not in self.page.services:
            self.page.services.append(self.picker)
            self.page.update()

    def will_unmount(self):
        if self.picker in self.page.services:
            self.page.services.remove(self.picker)

    def _select(self, e):
        self.selected_id = e.control.value
        self.snapshot = None
        self.download_button.disabled = True
        self._render_preview()
        self.update()

    def _generate(self, e):
        devices = [d for d in get_devices() if self.selected_id in ("all", d["id"])]
        device_ids = {d["id"] for d in devices}
        notifications = [n for n in get_notifications() if n["device_id"] in device_ids]
        self.snapshot = (devices, notifications, datetime.now())
        self.download_button.disabled = False
        self._render_preview()
        self.update()

    async def _download(self, e):
        if not self.snapshot:
            return
        devices, notifications, generated_at = self.snapshot
        try:
            pdf = create_report_pdf(devices, notifications, generated_at)
            filename = "IMK_relatorio_" + generated_at.strftime("%Y%m%d_%H%M") + ".pdf"
            await self.picker.save_file(dialog_title="Salvar relatório IMK", file_name=filename,
                                        file_type=ft.FilePickerFileType.CUSTOM,
                                        allowed_extensions=["pdf"], src_bytes=pdf)
        except Exception as exc:
            self.page.show_dialog(ft.SnackBar(ft.Text(f"Não foi possível salvar o PDF: {exc}")))

    def _render_preview(self):
        if not self.snapshot:
            self.preview.controls = [ft.Container(
                content=ft.Column([
                    ft.Icon(ft.Icons.ARTICLE_OUTLINED, color=TEXT_MUTED, size=36),
                    ft.Text("Selecione os dispositivos e clique em Gerar relatório.",
                            color=TEXT_MUTED, size=13),
                ], horizontal_alignment=ft.CrossAxisAlignment.CENTER, spacing=10),
                alignment=ft.Alignment.CENTER, height=170)]
            return
        devices, notices, generated_at = self.snapshot
        rows = []
        for device in devices:
            readings = "  ·  ".join(
                f"{title}: {format_value(device['values'][metric_id], unit)}"
                for metric_id, title, unit in METRICS
            )
            rows.append(ft.Container(ft.Column([
                ft.Row([ft.Text(device["name"], color=TEXT_WHITE, size=13,
                                weight=ft.FontWeight.BOLD),
                        label(device["device_id"], COLOR_GOOD)],
                       alignment=ft.MainAxisAlignment.SPACE_BETWEEN),
                label(f'{device["crop"]} · {device["area"]} · {device["status"]}'),
                ft.Text(readings, color="#cbd5e1", size=12),
            ], spacing=6), padding=12, bgcolor="#101720", border_radius=10))
        self.preview.controls = [
            ft.Row([label(generated_at.strftime("Gerado em %d/%m/%Y às %H:%M"), COLOR_BLUE),
                    label(f"{len(devices)} dispositivo(s) · {len(notices)} notificação(ões)", COLOR_WARNING)],
                   alignment=ft.MainAxisAlignment.SPACE_BETWEEN, wrap=True),
            *rows,
            label("Alertas e indicações incluídos:", "#cbd5e1", 12),
            *[ft.Text(f'• {n["title"]} — {n["location"]}', color=TEXT_MUTED, size=11) for n in notices],
            label("O PDF contém o mesmo conjunto de dados mostrado nesta prévia."),
        ]
