import flet as ft
from typing import List
from ...config import Theme, LABEL_COLORS, Spacing, Radius, Duration, Easing, Typography
from ...models import CardModel
from ..components import PriorityBadge, TagChip, DueDateBadge


def ListView(page, all_cards: List[CardModel], on_edit, on_delete):
    sorted_cards = sorted(all_cards, key=lambda c: ({4:0, 3:1, 2:2, 1:3}.get(c.priority, 4), c.title))
    rows = []
    for card in sorted_cards:
        tags = card.get_tags_list()
        color_name, color_hex = LABEL_COLORS.get(card.color, ("", Theme.TEXT_MUTED))
        rows.append(
            ft.Container(
                content=ft.Row([
                    ft.Container(width=4, height=48, border_radius=2, bgcolor=color_hex or Theme.BORDER_SUBTLE),
                    ft.Text(card.title, color=Theme.TEXT_PRIMARY, weight=ft.FontWeight.W_600, expand=True, size=Typography.BODY_MD),
                    ft.Row([TagChip(t) for t in tags[:2]], spacing=Spacing.XS, visible=len(tags) > 0),
                    PriorityBadge(card.priority),
                    DueDateBadge(card.due_date, card.is_overdue()),
                    ft.Text(card.assignee or "—", size=Typography.BODY_SM, color=Theme.TEXT_MUTED, width=120),
                    ft.Row([
                        ft.Container(content=ft.Icon(ft.Icons.EDIT_OUTLINED, color=Theme.NEON_BLUE, size=Typography.ICON), padding=8, border_radius=Radius.SM, on_click=lambda e, c=card: on_edit(c)),
                        ft.Container(content=ft.Icon(ft.Icons.DELETE_OUTLINED, color=Theme.NEON_RED, size=Typography.ICON), padding=8, border_radius=Radius.SM, on_click=lambda e, cid=card.id: page.run_task(on_delete, cid)),
                    ], spacing=0),
                ], spacing=Spacing.SM),
                bgcolor=Theme.BG_CARD, border_radius=Radius.MD, padding=ft.Padding.symmetric(horizontal=Spacing.SM, vertical=Spacing.SM),
                border=ft.Border.all(1, Theme.BORDER_SUBTLE), margin=ft.Margin.only(bottom=Spacing.XS),
                animate=ft.Animation(Duration.NORMAL, Easing.OUT),
            )
        )

    header = ft.Container(
        content=ft.Row([
            ft.Container(width=20),
            ft.Text("Titre", color=Theme.TEXT_SECONDARY, weight=ft.FontWeight.W_700, expand=True, size=Typography.BODY_SM),
            ft.Text("Tags", color=Theme.TEXT_SECONDARY, weight=ft.FontWeight.W_700, width=140, size=Typography.BODY_SM),
            ft.Text("Priorité", color=Theme.TEXT_SECONDARY, weight=ft.FontWeight.W_700, width=100, size=Typography.BODY_SM),
            ft.Text("Échéance", color=Theme.TEXT_SECONDARY, weight=ft.FontWeight.W_700, width=120, size=Typography.BODY_SM),
            ft.Text("Assigné", color=Theme.TEXT_SECONDARY, weight=ft.FontWeight.W_700, width=120, size=Typography.BODY_SM),
            ft.Container(width=100),
        ], spacing=Spacing.SM),
        padding=ft.Padding.symmetric(horizontal=Spacing.SM, vertical=Spacing.SM),
        bgcolor=Theme.BG_COLUMN, border_radius=Radius.MD, margin=ft.Margin.only(bottom=Spacing.SM),
    )

    list_column = ft.Column([
        ft.Row([ft.Icon(ft.Icons.LIST_ALT_ROUNDED, color=Theme.NEON_PURPLE, size=Typography.ICON_XL), ft.Text("Vue liste", size=Typography.H2, weight=ft.FontWeight.W_700, color=Theme.TEXT_PRIMARY)], spacing=Spacing.SM),
        ft.Divider(color=Theme.BORDER_SUBTLE),
        header,
        ft.Column(rows, spacing=0, scroll=ft.ScrollMode.AUTO, expand=True)
    ], spacing=Spacing.SM, expand=True)

    return ft.Container(content=list_column, padding=Spacing.LG, expand=True)
