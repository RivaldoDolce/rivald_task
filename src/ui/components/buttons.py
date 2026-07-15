import flet as ft
from ...config import Theme, Spacing, Radius, Duration, Easing, Typography


def NeonButton(text, on_click, icon=None, color=Theme.NEON_BLUE,
               expand=False, width=None, height=48):
    """Legacy button kept for backward compatibility. Prefer PrimaryButton."""
    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Icon(icon, color=color, size=Typography.ICON) if icon else ft.Container(),
                ft.Text(
                    text,
                    color=Theme.TEXT_PRIMARY,
                    weight=ft.FontWeight.W_600,
                    size=Typography.BODY,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=Spacing.XS,
        ),
        bgcolor=Theme.BG_ELEVATED,
        border_radius=Radius.MD,
        padding=ft.Padding.symmetric(horizontal=Spacing.SM, vertical=12),
        border=ft.Border.all(1, color + "44"),
        on_click=on_click,
        animate=ft.Animation(Duration.NORMAL, Easing.OUT),
        expand=expand,
        width=width,
        height=height,
        alignment=ft.Alignment(0, 0),
        on_hover=lambda e: None,
    )


def PrimaryButton(text, on_click, icon=None, expand=False, width=None, height=44):
    """Primary button — accent fill, dark text for high contrast."""
    def handle_hover(e):
        is_hover = e.data == "true"
        btn = e.control
        btn.bgcolor = "#6BA5FF" if is_hover else Theme.NEON_BLUE
        btn.shadow = (
            ft.BoxShadow(
                spread_radius=0, blur_radius=12,
                color=Theme.NEON_BLUE + "55", offset=ft.Offset(0, 2),
            )
            if is_hover else
            ft.BoxShadow(
                spread_radius=0, blur_radius=6,
                color=Theme.NEON_BLUE + "33", offset=ft.Offset(0, 1),
            )
        )
        btn.update()

    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Icon(icon, color=Theme.BG_GLOBAL, size=Typography.ICON_SM) if icon else ft.Container(),
                ft.Text(
                    text,
                    color=Theme.BG_GLOBAL,
                    weight=ft.FontWeight.W_700,
                    size=Typography.BODY,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=Spacing.XS,
        ),
        bgcolor=Theme.NEON_BLUE,
        border_radius=Radius.MD,
        padding=ft.Padding.symmetric(horizontal=Spacing.SM, vertical=10),
        on_click=on_click,
        on_hover=handle_hover,
        animate=ft.Animation(Duration.FAST, Easing.OUT),
        expand=expand,
        width=width,
        height=height,
        alignment=ft.Alignment(0, 0),
        shadow=ft.BoxShadow(
            spread_radius=0, blur_radius=6,
            color=Theme.NEON_BLUE + "33", offset=ft.Offset(0, 1),
        ),
    )


def GhostButton(text, on_click, icon=None, expand=False, width=None, height=40):
    """Ghost button — transparent background, subtle hover bg."""
    def handle_hover(e):
        is_hover = e.data == "true"
        btn = e.control
        btn.bgcolor = Theme.BG_ELEVATED if is_hover else None
        btn.update()

    return ft.Container(
        content=ft.Row(
            controls=[
                ft.Icon(icon, color=Theme.TEXT_SECONDARY, size=Typography.ICON_SM) if icon else ft.Container(),
                ft.Text(
                    text,
                    color=Theme.TEXT_SECONDARY,
                    weight=ft.FontWeight.W_500,
                    size=Typography.BODY,
                ),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
            spacing=Spacing.XS,
        ),
        border_radius=Radius.MD,
        padding=ft.Padding.symmetric(horizontal=Spacing.SM, vertical=10),
        on_click=on_click,
        on_hover=handle_hover,
        animate=ft.Animation(Duration.FAST, Easing.OUT),
        expand=expand,
        width=width,
        height=height,
        alignment=ft.Alignment(0, 0),
    )
