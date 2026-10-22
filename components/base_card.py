"""
Componente Base para todos os Cards do Dashboard STS.
Centraliza estilos padrão de container, bordas, arredondamento e espaçamento.
"""
import flet as ft
from theme import BG_CARD, BORDER_COLOR


class BaseCard(ft.Container):
    """
    Card base que padroniza o visual (background escuro, bordas arredondadas,
    borda sutil e padding interno). Todos os cards específicos herdam desta classe.
    """
    def __init__(
        self,
        content: ft.Control | None = None,
        padding: ft.Padding | None = None,
        border_radius: ft.BorderRadius | None = None,
        border: ft.Border | None = None,
        bgcolor: str = BG_CARD,
        expand: bool | int | None = None,
        width: int | float | None = None,
        height: int | float | None = None,
        **kwargs,
    ):
        super().__init__(
            content=content,
            bgcolor=bgcolor,
            border_radius=border_radius or ft.BorderRadius.all(16),
            border=border or ft.Border.all(1, BORDER_COLOR),
            padding=padding or ft.Padding.all(18),
            expand=expand,
            width=width,
            height=height,
            **kwargs,
        )

