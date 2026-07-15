import flet as ft
import json
from ...config import Theme, LABEL_COLORS, Typography, Radius, Spacing
from ...models import CardModel
from .priority_selector import PrioritySelector


def CardEditDialog(page, card: CardModel, on_save, on_close):
    title_val = ft.TextField(
        label="Titre", value=card.title,
        bgcolor=Theme.BG_INPUT, border_color=Theme.BORDER_SUBTLE,
        focused_border_color=Theme.NEON_BLUE,
        color=Theme.TEXT_PRIMARY, text_size=Typography.BODY,
        border_radius=Radius.MD,
    )
    desc_val = ft.TextField(
        label="Description", value=card.description or "",
        multiline=True, min_lines=3, max_lines=6,
        bgcolor=Theme.BG_INPUT, border_color=Theme.BORDER_SUBTLE,
        focused_border_color=Theme.NEON_BLUE,
        color=Theme.TEXT_PRIMARY, text_size=Typography.BODY_SM,
        border_radius=Radius.MD,
    )

    color_val = [card.color]
    color_row = ft.Row([], spacing=Spacing.XS, wrap=True)

    def set_color(k):
        color_val[0] = k
        for c in color_row.controls:
            c.border = ft.Border.all(1, Theme.TEXT_PRIMARY if color_val[0] == c.data else Theme.BORDER_SUBTLE)
            c.content.border = ft.Border.all(2, Theme.TEXT_PRIMARY if color_val[0] == c.data else "transparent")
            c.update()

    for k, (l, c) in LABEL_COLORS.items():
        if c:
            cont = ft.Container(
                content=ft.Container(
                    width=36, height=36, border_radius=Radius.MD, bgcolor=c,
                    border=ft.Border.all(2, Theme.TEXT_PRIMARY if color_val[0] == k else "transparent"),
                ),
                padding=5, border_radius=Radius.MD,
                border=ft.Border.all(1, Theme.TEXT_PRIMARY if color_val[0] == k else Theme.BORDER_SUBTLE),
                on_click=lambda e, k=k: set_color(k),
                animate=ft.Animation(200, ft.AnimationCurve.EASE_OUT),
            )
            cont.data = k
            color_row.controls.append(cont)

    priority_row, priority_val = PrioritySelector(card.priority, lambda p: None)

    tags_val = ft.TextField(
        value=", ".join(card.get_tags_list()),
        bgcolor=Theme.BG_INPUT, border_color=Theme.BORDER_SUBTLE,
        focused_border_color=Theme.NEON_BLUE,
        color=Theme.TEXT_PRIMARY, hint_text="bug, urgent...",
        text_size=Typography.BODY_SM, border_radius=Radius.MD,
    )
    due_val = ft.TextField(
        value=card.due_date or "",
        bgcolor=Theme.BG_INPUT, border_color=Theme.BORDER_SUBTLE,
        focused_border_color=Theme.NEON_BLUE,
        color=Theme.TEXT_PRIMARY, hint_text="AAAA-MM-JJ",
        text_size=Typography.BODY_SM, border_radius=Radius.MD,
    )
    assignee_val = ft.TextField(
        value=card.assignee or "",
        bgcolor=Theme.BG_INPUT, border_color=Theme.BORDER_SUBTLE,
        focused_border_color=Theme.NEON_BLUE,
        color=Theme.TEXT_PRIMARY, prefix_icon=ft.Icons.PERSON_OUTLINED,
        text_size=Typography.BODY_SM, border_radius=Radius.MD,
    )

    async def save(e):
        await on_save(
            card.id, title_val.value, desc_val.value, color_val[0], priority_val[0],
            json.dumps([t.strip() for t in tags_val.value.split(",") if t.strip()]),
            due_val.value or None, assignee_val.value or None
        )
        on_close()

    dlg = ft.AlertDialog(
        title=ft.Row(
            [ft.Icon(ft.Icons.EDIT_NOTE_ROUNDED, color=Theme.NEON_BLUE, size=Typography.ICON_XL),
             ft.Text("Éditer la carte", size=Typography.H3,
                     weight=ft.FontWeight.W_700, color=Theme.TEXT_PRIMARY)],
            spacing=Spacing.SM,
        ),
        content=ft.Container(
            content=ft.Column([
                title_val, desc_val,
                ft.Text("Étiquette", size=Typography.BODY_SM, color=Theme.TEXT_SECONDARY,
                        weight=ft.FontWeight.W_700), color_row,
                ft.Text("Priorité", size=Typography.BODY_SM, color=Theme.TEXT_SECONDARY,
                        weight=ft.FontWeight.W_700), priority_row,
                ft.Row([ft.Column([ft.Text("Tags", size=Typography.BODY_SM, color=Theme.TEXT_SECONDARY), tags_val], expand=True),
                        ft.Column([ft.Text("Échéance", size=Typography.BODY_SM, color=Theme.TEXT_SECONDARY), due_val], expand=True)],
                       spacing=Spacing.SM),
                assignee_val
            ], spacing=Spacing.SM, tight=True, scroll=ft.ScrollMode.AUTO),
            width=560, padding=Spacing.SM,
        ),
        actions=[
            ft.TextButton("Annuler", on_click=lambda e: on_close()),
            ft.FilledButton("Sauvegarder", on_click=save, bgcolor=Theme.NEON_BLUE, color=Theme.BG_GLOBAL)
        ],
        bgcolor=Theme.BG_COLUMN, shape=ft.RoundedRectangleBorder(radius=Radius.XL),
    )
    page.overlay.append(dlg)
    return dlg
