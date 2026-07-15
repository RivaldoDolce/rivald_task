import flet as ft
from ...config import Theme, Typography, Radius, Spacing


def PrioritySelector(default_priority: int, on_change):
    """Priority selector with custom buttons — replaces the flaky SegmentedButton."""
    priority_val = [default_priority]
    priority_data = [
        (1, "Basse", Theme.NEON_GREEN),
        (2, "Moyenne", Theme.NEON_BLUE),
        (3, "Haute", Theme.NEON_ORANGE),
        (4, "Critique", Theme.NEON_RED),
    ]
    buttons = []

    def set_priority(p):
        priority_val[0] = p
        for btn in buttons:
            active = btn.data == p
            btn.bgcolor = Theme.BG_ELEVATED if active else Theme.BG_INPUT
            btn.border = ft.Border.all(1, (btn.content.color if active else Theme.BORDER_SUBTLE))
            btn.update()
        on_change(p)

    for p, label, color in priority_data:
        btn = ft.Container(
            content=ft.Text(label, size=Typography.BODY_XS,
                            weight=ft.FontWeight.W_700, color=color),
            data=p,
            bgcolor=Theme.BG_ELEVATED if p == default_priority else Theme.BG_INPUT,
            border_radius=Radius.MD,
            padding=ft.Padding.symmetric(horizontal=Spacing.SM, vertical=10),
            border=ft.Border.all(1, color if p == default_priority else Theme.BORDER_SUBTLE),
            on_click=lambda e, p=p: set_priority(p),
            animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
            alignment=ft.Alignment(0, 0),
        )
        buttons.append(btn)

    return ft.Row(buttons, spacing=Spacing.XS), priority_val
