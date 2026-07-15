"""
Mobile analytics view.

On mobile, counters stack vertically (one per row) and distribution cards
are stacked below. This avoids the cramped side-by-side layout that breaks
on narrow screens.
"""
import flet as ft
from typing import List
from ...config import Theme, Spacing, Radius, Duration, Easing, Typography
from ...models import CardModel, ColumnModel
from ..components import AnimatedCounter, GlassCard, ProgressBarCustom


def MobileAnalyticsView(all_cards: List[CardModel], columns: List[ColumnModel]):
    total_cards = len(all_cards)
    by_priority = {1: 0, 2: 0, 3: 0, 4: 0}
    by_color = {}
    overdue_count = 0

    for card in all_cards:
        by_priority[card.priority] = by_priority.get(card.priority, 0) + 1
        if card.color != "transparent":
            by_color[card.color] = by_color.get(card.color, 0) + 1
        if card.is_overdue():
            overdue_count += 1

    col_distribution = []
    for col in columns:
        count = len([c for c in all_cards if c.column_id == col.id])
        col_distribution.append((col.title, count, col.color))

    priority_colors = {1: Theme.NEON_GREEN, 2: Theme.NEON_BLUE, 3: Theme.NEON_ORANGE, 4: Theme.NEON_RED}
    priority_labels = {1: "Basse", 2: "Moyenne", 3: "Haute", 4: "Critique"}

    # Counters stacked vertically (1 per row on mobile).
    counters = ft.Column(
        controls=[
            AnimatedCounter(total_cards, "Total cartes", Theme.NEON_BLUE),
            AnimatedCounter(overdue_count, "En retard", Theme.NEON_RED),
            AnimatedCounter(sum(1 for c in all_cards if c.assignee), "Assignees", Theme.NEON_PURPLE),
            AnimatedCounter(len(by_color), "Etiquettes actives", Theme.NEON_GREEN),
        ],
        spacing=Spacing.SM,
    )

    # Priority distribution — bars use full available width.
    priority_bars = ft.Column(
        controls=[
            ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Text(priority_labels[p], size=Typography.BODY_SM,
                                    color=Theme.TEXT_SECONDARY, width=80),
                            ft.Text(str(by_priority[p]), size=Typography.BODY_SM,
                                    color=Theme.TEXT_PRIMARY,
                                    weight=ft.FontWeight.W_700, width=32),
                        ],
                        spacing=Spacing.XS,
                    ),
                    ProgressBarCustom(by_priority[p] / max(total_cards, 1),
                                       color=priority_colors[p], width=None),
                ],
                spacing=4,
            )
            for p in [4, 3, 2, 1]
        ],
        spacing=Spacing.XS,
    )

    col_bars = ft.Column(
        controls=[
            ft.Column(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Container(width=14, height=14, border_radius=4, bgcolor=color),
                            ft.Text(title, size=Typography.BODY_SM,
                                    color=Theme.TEXT_SECONDARY, expand=True),
                            ft.Text(str(count), size=Typography.BODY_SM,
                                    color=Theme.TEXT_PRIMARY,
                                    weight=ft.FontWeight.W_700, width=32),
                        ],
                        spacing=Spacing.XS,
                    ),
                    ProgressBarCustom(count / max(total_cards, 1),
                                       color=color, width=None),
                ],
                spacing=4,
            )
            for title, count, color in col_distribution
        ],
        spacing=Spacing.XS,
    )

    content = ft.Column(
        controls=[
            ft.Row(
                controls=[
                    ft.Icon(ft.Icons.INSIGHTS_ROUNDED, color=Theme.NEON_GREEN,
                            size=Typography.ICON_XL),
                    ft.Text("Tableau de bord", size=Typography.H3,
                            weight=ft.FontWeight.W_700, color=Theme.TEXT_PRIMARY),
                ],
                spacing=Spacing.SM,
            ),
            ft.Divider(color=Theme.BORDER_SUBTLE),
            counters,
            GlassCard(
                ft.Column(
                    controls=[
                        ft.Text("Distribution par priorite", size=Typography.BODY_LG,
                                weight=ft.FontWeight.W_700, color=Theme.TEXT_PRIMARY),
                        priority_bars,
                    ],
                    spacing=Spacing.SM,
                ),
            ),
            GlassCard(
                ft.Column(
                    controls=[
                        ft.Text("Distribution par colonne", size=Typography.BODY_LG,
                                weight=ft.FontWeight.W_700, color=Theme.TEXT_PRIMARY),
                        col_bars,
                    ],
                    spacing=Spacing.SM,
                ),
            ),
        ],
        spacing=Spacing.MD,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )

    return ft.Container(
        content=content,
        padding=Spacing.SM,
        expand=True,
    )
