"""Small dependency-free A4 PDF renderer for the current report snapshot.

Uses PDF standard fonts with WinAnsiEncoding for Portuguese text. The output
is kept deliberately text based so it can be opened and searched anywhere.
"""
from datetime import datetime
from textwrap import wrap

from telemetry import METRICS, format_value


def _literal(value):
    raw = str(value).replace("\u2014", "-").replace("\u2013", "-").encode("cp1252", "replace")
    return b"(" + raw.replace(b"\\", b"\\\\").replace(b"(", b"\\(").replace(b")", b"\\)") + b")"


def create_report_pdf(devices, notifications, generated_at=None):
    """Generate a multi-page PDF from the exact snapshot shown in the preview."""
    generated_at = generated_at or datetime.now()
    pages = []
    commands = []
    y = 790
    page_number = 0

    def line(text, size=10, bold=False, color=(0.12, 0.18, 0.24), indent=0, step=None):
        nonlocal y
        if y < 70:
            new_page()
        r, g, b = color
        font = "F2" if bold else "F1"
        commands.append(b"BT %.3f %.3f %.3f rg /%s %d Tf 1 0 0 1 %d %d Tm %s Tj ET" %
                        (r, g, b, font.encode(), size, 48 + indent, y, _literal(text)))
        y -= step or (size + 8)

    def separator():
        nonlocal y
        commands.append(b"0.83 0.87 0.89 RG 48 %d m 547 %d l S" % (y, y))
        y -= 18

    def new_page():
        nonlocal commands, y, page_number
        if commands:
            pages.append(b"\n".join(commands))
        page_number += 1
        commands = [
            b"0.04 0.10 0.14 rg 0 810 595 32 re f",
            b"0.05 0.72 0.52 rg 48 813 9 9 re f",
            b"BT 0.92 0.96 0.96 rg /F2 11 Tf 1 0 0 1 65 813 Tm (IMK  |  RELATORIO AGRICOLA) Tj ET",
            b"BT 0.43 0.49 0.54 rg /F1 8 Tf 1 0 0 1 48 35 Tm " + _literal(f"Fazenda Santa Maria  |  Dados de demonstração  |  Página {page_number}") + b" Tj ET",
        ]
        y = 780

    new_page()
    line("Relatório de monitoramento", 20, True, step=31)
    line("Fazenda Santa Maria  |  Safra 2026/2027", 11, step=23)
    line("Gerado em " + generated_at.strftime("%d/%m/%Y às %H:%M"), 10, step=24)
    line("Fonte: dados de demonstração do dashboard IMK. Não representam medições ao vivo.", 9,
         color=(0.40, 0.45, 0.50), step=24)
    separator()
    line("Resumo", 14, True, step=24)
    online_count = sum(d["online"] for d in devices)
    line(f"Dispositivos no relatório: {len(devices)}  |  Online: {online_count}  |  Offline: {len(devices) - online_count}")
    line(f"Notificações relacionadas: {len(notifications)}", step=25)
    separator()
    line("Leituras por dispositivo", 14, True, step=24)
    for device in devices:
        if y < 195:
            new_page()
        line(f'{device["name"]}  |  {device["device_id"]}', 12, True, step=19)
        line(f'{device["crop"]}  |  {device["area"]}  |  {device["status"]}', 9,
             color=(0.40, 0.45, 0.50), step=18)
        for metric_id, title, unit in METRICS:
            line(f'{title}: {format_value(device["values"][metric_id], unit)}', 10, indent=12, step=17)
        y -= 10
    if y < 195:
        new_page()
    separator()
    line("Alertas e indicações", 14, True, step=24)
    if not notifications:
        line("Nenhuma notificação para os dispositivos selecionados.")
    for notice in notifications:
        if y < 145:
            new_page()
        line(f'{notice["category"]} · {notice["severity"]}  |  {notice["location"]}', 9, True,
             color=(0.68, 0.36, 0.04) if notice["category"] == "Alerta" else (0.05, 0.48, 0.39), step=17)
        for part in wrap(notice["title"], width=80):
            line(part, 10, True, step=16)
        for part in wrap(notice["description"], width=90):
            line(part, 9, indent=8, step=15)
        y -= 9
    pages.append(b"\n".join(commands))

    # Object numbers: catalog 1, pages 2, fonts 3-4, then page/content pairs.
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [" + b" ".join(f"{5 + 2*i} 0 R".encode() for i in range(len(pages))) +
        b"] /Count " + str(len(pages)).encode() + b" >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica /Encoding /WinAnsiEncoding >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold /Encoding /WinAnsiEncoding >>",
    ]
    for i, page in enumerate(pages):
        stream = page
        objects.append(b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] /Resources << /Font << /F1 3 0 R /F2 4 0 R >> >> /Contents " +
                       str(6 + 2*i).encode() + b" 0 R >>")
        objects.append(b"<< /Length " + str(len(stream)).encode() + b" >>\nstream\n" + stream + b"\nendstream")
    output = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0]
    for number, obj in enumerate(objects, 1):
        offsets.append(len(output))
        output.extend(f"{number} 0 obj\n".encode() + obj + b"\nendobj\n")
    xref = len(output)
    output.extend(f"xref\n0 {len(objects)+1}\n0000000000 65535 f \n".encode())
    for offset in offsets[1:]:
        output.extend(f"{offset:010d} 00000 n \n".encode())
    output.extend(b"trailer\n<< /Size " + str(len(objects)+1).encode() +
                  b" /Root 1 0 R >>\nstartxref\n" + str(xref).encode() + b"\n%%EOF\n")
    return bytes(output)
