import flet as ft
from typing import List
from ...config import Theme, Spacing, Radius, Duration, Easing, Typography
from ...models import CardModel, ColumnModel
from ..components import AnimatedCounter, GlassCard, ProgressBarCustom


def AnalyticsView(all_cards: List[CardModel], columns: List[ColumnModel]):
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

    stats_row = ft.Row([
        AnimatedCounter(total_cards, "Total cartes", Theme.NEON_BLUE),
        AnimatedCounter(overdue_count, "En retard", Theme.NEON_RED),
        AnimatedCounter(sum(1 for c in all_cards if c.assignee), "Assignées", Theme.NEON_PURPLE),
        AnimatedCounter(len(by_color), "Étiquettes actives", Theme.NEON_GREEN),
    ], spacing=Spacing.SM)

    priority_bars = ft.Column([
        ft.Row([
            ft.Text(priority_labels[p], size=Typography.BODY_SM, color=Theme.TEXT_SECONDARY, width=100),
            ProgressBarCustom(by_priority[p] / max(total_cards, 1), color=priority_colors[p], width=320),
            ft.Text(str(by_priority[p]), size=Typography.BODY_SM, color=Theme.TEXT_PRIMARY, weight=ft.FontWeight.W_700, width=48),
        ], spacing=Spacing.SM) for p in [4, 3, 2, 1]
    ], spacing=Spacing.XS)

    col_bars = ft.Column([
        ft.Row([
            ft.Container(width=16, height=16, border_radius=4, bgcolor=color),
            ft.Text(title, size=Typography.BODY_SM, color=Theme.TEXT_SECONDARY, width=140),
            ProgressBarCustom(count / max(total_cards, 1), color=color, width=260),
            ft.Text(str(count), size=Typography.BODY_SM, color=Theme.TEXT_PRIMARY, weight=ft.FontWeight.W_700, width=48),
        ], spacing=Spacing.SM) for title, count, color in col_distribution
    ], spacing=Spacing.XS)

    content = ft.Column([
        ft.Row([ft.Icon(ft.Icons.INSIGHTS_ROUNDED, color=Theme.NEON_GREEN, size=Typography.ICON_XL), ft.Text("Tableau de bord analytique", size=Typography.H2, weight=ft.FontWeight.W_700, color=Theme.TEXT_PRIMARY)], spacing=Spacing.SM),
        ft.Divider(color=Theme.BORDER_SUBTLE),
        stats_row,
        ft.Row([
            GlassCard(ft.Column([ft.Text("Distribution par priorité", size=Typography.BODY_LG, weight=ft.FontWeight.W_700, color=Theme.TEXT_PRIMARY), priority_bars], spacing=Spacing.SM), expand=True),
            GlassCard(ft.Column([ft.Text("Distribution par colonne", size=Typography.BODY_LG, weight=ft.FontWeight.W_700, color=Theme.TEXT_PRIMARY), col_bars], spacing=Spacing.SM), expand=True),
        ], spacing=Spacing.SM)
    ], spacing=Spacing.MD, scroll=ft.ScrollMode.AUTO, expand=True)

    return ft.Container(content=content, padding=Spacing.LG, expand=True)
