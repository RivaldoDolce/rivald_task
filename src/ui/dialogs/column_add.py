import flet as ft
from ...config import Theme, Typography, Radius, Spacing


def AddColumnDialog(page, on_save, on_close):
    title_val = ft.TextField(
        label="Nom de la colonne", autofocus=True,
        bgcolor=Theme.BG_INPUT, border_color=Theme.BORDER_SUBTLE,
        focused_border_color=Theme.NEON_PURPLE,
        color=Theme.TEXT_PRIMARY, text_size=Typography.BODY,
        border_radius=Radius.MD,
    )
    color_val = ["#1E293B"]

    color_options = [
        ("#1E293B", "Gris"), ("#3B9EFF", "Bleu"), ("#4ADE80", "Vert"),
        ("#FB923C", "Orange"), ("#B47CFF", "Violet"), ("#F87171", "Rouge"),
        ("#22D3EE", "Cyan"), ("#FF7AC4", "Rose"),
    ]
    color_row = ft.Row([
        ft.Container(
            width=40, height=40, border_radius=Radius.MD, bgcolor=c,
            border=ft.Border.all(2, Theme.TEXT_PRIMARY if color_val[0] == c else "transparent"),
            on_click=lambda e, c=c: set_color(c),
            animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
        ) for c, _ in color_options
    ], spacing=Spacing.XS, wrap=True)

    def set_color(c):
        color_val[0] = c
        for cont in color_row.controls:
            cont.border = ft.Border.all(2, Theme.TEXT_PRIMARY if color_val[0] == cont.bgcolor else "transparent")
            cont.update()

    async def save(e):
        if title_val.value and title_val.value.strip():
            await on_save(title_val.value.strip(), color_val[0])
            on_close()

    dlg = ft.AlertDialog(
        title=ft.Row(
            [ft.Icon(ft.Icons.VIEW_COLUMN_ROUNDED, color=Theme.NEON_PURPLE, size=Typography.ICON_XL),
             ft.Text("Nouvelle colonne", size=Typography.H3,
                     weight=ft.FontWeight.W_700, color=Theme.TEXT_PRIMARY)],
            spacing=Spacing.SM,
        ),
        content=ft.Container(
            content=ft.Column([
                title_val,
                ft.Text("Couleur", size=Typography.BODY_SM, color=Theme.TEXT_SECONDARY,
                        weight=ft.FontWeight.W_700),
                color_row
            ], spacing=Spacing.SM, tight=True),
            width=440, padding=Spacing.SM,
        ),
        actions=[
            ft.TextButton("Annuler", on_click=lambda e: on_close()),
            ft.FilledButton("Créer", on_click=save, bgcolor=Theme.NEON_PURPLE, color=Theme.BG_GLOBAL)
        ],
        bgcolor=Theme.BG_COLUMN, shape=ft.RoundedRectangleBorder(radius=Radius.XL),
    )
    page.overlay.append(dlg)
    return dlg
