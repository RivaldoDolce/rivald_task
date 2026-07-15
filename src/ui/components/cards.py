import flet as ft
from ...config import Theme, Spacing, Radius, Duration, Easing, Typography


def GlassCard(content, padding=Spacing.SM, border_radius=Radius.LG,
              border_color=Theme.BORDER_SUBTLE, glow_color=None,
              expand=False, width=None, height=None):
    """Glass card — subtle border, natural shadow. No permanent halo."""
    def make_shadow(glow):
        if glow and glow_color:
            return [
                ft.BoxShadow(
                    spread_radius=0, blur_radius=18,
                    color=glow_color + "22", offset=ft.Offset(0, 4),
                ),
                Theme.SHADOW_CARD,
            ]
        return [Theme.SHADOW_CARD]

    container = ft.Container(
        content=content,
        bgcolor=Theme.BG_CARD,
        border_radius=border_radius,
        padding=padding,
        border=ft.Border.all(1, border_color),
        shadow=make_shadow(False),
        expand=expand,
        width=width,
        height=height,
        animate=ft.Animation(Duration.NORMAL, Easing.OUT),
    )

    if glow_color:
        def on_hover(e):
            is_hover = e.data == "true"
            container.shadow = make_shadow(is_hover)
            container.border = ft.Border.all(
                1, glow_color + "44" if is_hover else border_color
            )
            container.update()
        container.on_hover = on_hover

    return container


def AnimatedCounter(value: int, label: str, color: str = Theme.NEON_BLUE):
    """Analytics counter — accent color only on the value."""
    return ft.Container(
        content=ft.Column(
            controls=[
                ft.Text(
                    str(value), size=Typography.COUNTER,
                    weight=ft.FontWeight.W_700, color=color,
                ),
                ft.Text(
                    label, size=Typography.BODY_SM,
                    color=Theme.TEXT_SECONDARY,
                    weight=ft.FontWeight.W_500,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
        ),
        bgcolor=Theme.BG_CARD,
        border_radius=Radius.LG,
        padding=Spacing.MD,
        border=ft.Border.all(1, Theme.BORDER_SUBTLE),
        shadow=Theme.SHADOW_CARD,
        expand=True,
        alignment=ft.Alignment(0, 0),
    )
