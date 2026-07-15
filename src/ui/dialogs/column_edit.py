import flet as ft
from ...config import Theme, Typography, Radius, Spacing


def ColumnEditDialog(page, col, on_save, on_close):
    title_f = ft.TextField(
        value=col.title, autofocus=True,
        bgcolor=Theme.BG_INPUT, border_color=Theme.BORDER_SUBTLE,
        focused_border_color=Theme.NEON_BLUE,
        color=Theme.TEXT_PRIMARY, text_size=Typography.BODY,
        border_radius=Radius.MD,
    )

    async def save_and_close(e):
        if title_f.value and title_f.value.strip():
            await on_save(col.id, title_f.value.strip())
            on_close()

    dlg = ft.AlertDialog(
        title=ft.Row(
            [ft.Icon(ft.Icons.EDIT_OUTLINED, color=Theme.NEON_BLUE, size=Typography.ICON_XL),
             ft.Text("Renommer la colonne", size=Typography.H3,
                     weight=ft.FontWeight.W_700, color=Theme.TEXT_PRIMARY)],
            spacing=Spacing.SM,
        ),
        content=ft.Container(
            content=title_f,
            width=440,
            padding=ft.Padding.only(top=Spacing.XS),
        ),
        actions=[
            ft.TextButton("Annuler", on_click=lambda e: on_close()),
            ft.FilledButton("Sauvegarder", on_click=save_and_close,
                            bgcolor=Theme.NEON_BLUE, color=Theme.BG_GLOBAL),
        ],
        bgcolor=Theme.BG_COLUMN,
        shape=ft.RoundedRectangleBorder(radius=Radius.XL),
    )
    page.overlay.append(dlg)
    return dlg
