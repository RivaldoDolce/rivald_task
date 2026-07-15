import flet as ft
from ...config import Theme, Radius


def ProgressBarCustom(value: float, color: str = Theme.NEON_BLUE,
                      height: int = 6, width=None):
    """
    Progress bar. If width=None, the bar expands to fill its parent.
    Otherwise, a fixed width (in pixels) is used.
    """
    fill_value = width * min(max(value, 0.0), 1.0) if width is not None else None

    return ft.Container(
        content=ft.Stack(
            controls=[
                ft.Container(
                    bgcolor=Theme.BG_INPUT,
                    border_radius=height // 2,
                    height=height,
                    width=width,
                    expand=(width is None),
                ),
                ft.Container(
                    bgcolor=color,
                    border_radius=height // 2,
                    height=height,
                    width=fill_value,
                    expand=(width is None and fill_value is None),
                ),
            ],
        ),
        height=height,
        width=width,
        expand=(width is None),
    )
