import flet as ft
from typing import Optional
from ...config import Theme, Radius, Duration, Easing, Typography


def PriorityBadge(priority: int):
    """Priority badge — discreet tinted background, no permanent halo."""
    colors = {
        1: ("Basse", Theme.NEON_GREEN),
        2: ("Moyenne", Theme.NEON_BLUE),
        3: ("Haute", Theme.NEON_ORANGE),
        4: ("Critique", Theme.NEON_RED),
    }
    label, color = colors.get(priority, ("Inconnu", Theme.TEXT_MUTED))
    return ft.Container(
        content=ft.Text(
            label, size=Typography.BODY_XS,
            weight=ft.FontWeight.W_700,
            color=color,
        ),
        bgcolor=color + "1F",
        border_radius=Radius.SM,
        padding=ft.Padding.symmetric(horizontal=8, vertical=4),
        border=ft.Border.all(1, color + "33"),
        animate=ft.Animation(Duration.FAST, Easing.OUT),
    )


def TagChip(tag_text: str, color: str = Theme.NEON_BLUE):
    """Tag chip — very discreet, Linear-style."""
    return ft.Container(
        content=ft.Text(
            tag_text, size=Typography.BODY_XS,
            color=Theme.TEXT_SECONDARY,
            weight=ft.FontWeight.W_600,
        ),
        bgcolor=Theme.BG_INPUT,
        border_radius=Radius.SM,
        padding=ft.Padding.symmetric(horizontal=8, vertical=4),
        border=ft.Border.all(1, Theme.BORDER_SUBTLE),
    )


def DueDateBadge(due_date: Optional[str], is_overdue: bool = False):
    """Due date badge — discreet, red if overdue."""
    if not due_date:
        return ft.Container()
    color = Theme.NEON_RED if is_overdue else Theme.TEXT_MUTED
    icon = (ft.Icons.WARNING_AMBER_ROUNDED
            if is_overdue else ft.Icons.EVENT_AVAILABLE_ROUNDED)
    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Icon(icon, color=color, size=Typography.ICON_XS),
                ft.Text(
                    due_date, size=Typography.BODY_XS,
                    color=color, weight=ft.FontWeight.W_600,
                ),
            ],
            spacing=4,
        ),
        bgcolor=color + "14",
        border_radius=Radius.SM,
        padding=ft.Padding.symmetric(horizontal=8, vertical=4),
    )
