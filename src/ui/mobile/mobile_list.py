"""
Mobile list view.

Single-column simplified list. Each card is a touch-friendly row with
larger tap targets. Edit/delete icons are always visible (not on hover).
"""
import flet as ft
from typing import List
from ...config import Theme, LABEL_COLORS, Spacing, Radius, Duration, Easing, Typography
from ...models import CardModel
from ..components import PriorityBadge, TagChip, DueDateBadge


def MobileListView(page, all_cards: List[CardModel], on_edit, on_delete):
    sorted_cards = sorted(all_cards, key=lambda c: ({4:0, 3:1, 2:2, 1:3}.get(c.priority, 4), c.title))

    rows = []
    for card in sorted_cards:
        tags = card.get_tags_list()
        color_name, color_hex = LABEL_COLORS.get(card.color, ("", Theme.TEXT_MUTED))
        rows.append(
            ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Row(
                            controls=[
                                ft.Container(
                                    width=4, height=40, border_radius=2,
                                    bgcolor=color_hex or Theme.BORDER_SUBTLE,
                                ),
                                ft.Text(
                                    card.title,
                                    color=Theme.TEXT_PRIMARY,
                                    weight=ft.FontWeight.W_600,
                                    size=Typography.BODY_MD,
                                    expand=True,
                                ),
                                ft.IconButton(
                                    ft.Icons.EDIT_OUTLINED,
                                    icon_color=Theme.NEON_BLUE,
                                    icon_size=Typography.ICON,
                                    on_click=lambda e, c=card: on_edit(c),
                                    style=ft.ButtonStyle(padding=8),
                                ),
                                ft.IconButton(
                                    ft.Icons.DELETE_OUTLINE_ROUNDED,
                                    icon_color=Theme.NEON_RED,
                                    icon_size=Typography.ICON,
                                    on_click=lambda e, cid=card.id: page.run_task(on_delete, cid),
                                    style=ft.ButtonStyle(padding=8),
                                ),
                            ],
                            spacing=Spacing.XS,
                        ),
                        ft.Row(
                            controls=[
                                PriorityBadge(card.priority),
                                DueDateBadge(card.due_date, card.is_overdue()),
                            ] + [TagChip(t) for t in tags[:2]],
                            spacing=Spacing.XS,
                            wrap=True,
                        ),
                        ft.Row(
                            controls=[
                                ft.Text(
                                    card.assignee or "Non assigne",
                                    size=Typography.BODY_XS,
                                    color=Theme.TEXT_MUTED,
                                ),
                            ],
                        ),
                    ],
                    spacing=Spacing.XS,
                ),
                bgcolor=Theme.BG_CARD,
                border_radius=Radius.MD,
                padding=Spacing.SM,
                border=ft.Border.all(1, Theme.BORDER_SUBTLE),
                margin=ft.Margin.only(bottom=Spacing.XS),
                animate=ft.Animation(Duration.NORMAL, Easing.OUT),
            )
        )

    if not rows:
        empty = ft.Container(
            content=ft.Column(
                [
                    ft.Icon(ft.Icons.LIST_ALT_ROUNDED, color=Theme.TEXT_MUTED, size=64),
                    ft.Text("Aucune tache", color=Theme.TEXT_SECONDARY, size=Typography.H3),
                    ft.Text("Les taches appearont ici.", color=Theme.TEXT_MUTED, size=Typography.BODY),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=Spacing.SM,
            ),
            expand=True,
            alignment=ft.Alignment(0, 0),
            padding=Spacing.LG,
        )
        return ft.Container(content=empty, expand=True)

    list_column = ft.Column(
        controls=[
            ft.Row(
                controls=[
                    ft.Icon(ft.Icons.LIST_ALT_ROUNDED, color=Theme.NEON_PURPLE,
                            size=Typography.ICON_XL),
                    ft.Text("Vue liste", size=Typography.H3,
                            weight=ft.FontWeight.W_700, color=Theme.TEXT_PRIMARY),
                ],
                spacing=Spacing.SM,
            ),
            ft.Divider(color=Theme.BORDER_SUBTLE),
            ft.Column(rows, spacing=0, scroll=ft.ScrollMode.AUTO, expand=True),
        ],
        spacing=Spacing.SM,
        expand=True,
    )

    return ft.Container(content=list_column, padding=Spacing.SM, expand=True)
