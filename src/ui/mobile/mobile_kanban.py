"""
Mobile Kanban view.

On mobile, we replace the multi-column grid with a TabBar + TabBarView:
- One tab per column in the TabBar.
- The TabBarView contains one Column view per tab.
- Horizontal swipe between tabs (Flet TabBarView supports this natively).
- "Add task" button at the bottom of each tab.
- The cards list area has a dynamic height based on card count, with a
  minimum and maximum. When cards exceed the maximum, the list scrolls
  vertically inside its allocated area.

This is the pattern used by Trello, Notion and ClickUp mobile apps.
"""
import flet as ft
from typing import List
from ...config import (
    Theme, Layout, Spacing, Radius, Duration, Easing, Typography,
)
from ...models import ColumnModel, CardModel
from ..kanban.task_card import TaskCard


def MobileKanbanView(page, app_state, app):
    """Build the mobile Kanban view: TabBar at top, one column per tab."""
    filtered_cards = app_state.get_filtered_cards()

    if not app_state.columns:
        return ft.Container(
            content=ft.Column(
                [
                    ft.Icon(ft.Icons.VIEW_KANBAN_OUTLINED,
                            color=Theme.TEXT_MUTED, size=64),
                    ft.Text("Aucune colonne",
                            color=Theme.TEXT_SECONDARY, size=Typography.H3),
                    ft.Text("Creez une colonne pour commencer.",
                            color=Theme.TEXT_MUTED, size=Typography.BODY),
                ],
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=Spacing.SM,
            ),
            expand=True,
            alignment=ft.Alignment(0, 0),
            padding=Spacing.LG,
        )

    # Build the tab labels and the tab contents.
    tab_labels = []
    tab_contents = []
    for col in app_state.columns:
        col_cards = [c for c in filtered_cards if c.column_id == col.id]
        tab_labels.append(ft.Tab(label=col.title))
        tab_contents.append(_build_column_content(page, col, col_cards, app))

    tab_bar = ft.TabBar(
        tabs=tab_labels,
        scrollable=True,
        tab_alignment=ft.TabAlignment.START,
        divider_color=Theme.BORDER_SUBTLE,
        indicator_color=Theme.NEON_BLUE,
        label_color=Theme.TEXT_PRIMARY,
        unselected_label_color=Theme.TEXT_MUTED,
        indicator_size=ft.TabBarIndicatorSize.LABEL,
    )

    tab_bar_view = ft.TabBarView(
        controls=tab_contents,
        expand=True,
    )

    # NOTE: In Flet 0.85.3, TabBar and TabBarView MUST be placed inside a
    # ft.Tabs control. The Tabs control acts as the TabController that
    # coordinates the selected_index between the TabBar and the TabBarView.
    # Without this wrapper, Flet raises:
    #   "TabBar must be used within a Tabs control"
    #   "TabBarView must be used within a Tabs control"
    # The `length` parameter must equal the number of tabs.
    tabs = ft.Tabs(
        content=ft.Column(
            controls=[tab_bar, tab_bar_view],
            spacing=0,
            expand=True,
        ),
        length=len(tab_labels),
        selected_index=0,
        expand=True,
    )

    return tabs


def _calc_mobile_cards_list_height(num_cards: int) -> float:
    """
    Calculate the height of the cards list area based on card count.

    - Minimum height: Layout.MOBILE_MIN_COLUMN_HEIGHT (280px).
    - Each card adds ~Layout.MOBILE_CARD_HEIGHT_ESTIMATE (110px).
    - Maximum height: Layout.MOBILE_MAX_COLUMN_HEIGHT (600px).

    When the content exceeds the calculated height, the Column scrolls
    vertically (scroll=ft.ScrollMode.AUTO).
    """
    natural = (
        Layout.MOBILE_MIN_COLUMN_HEIGHT
        + max(0, num_cards) * Layout.MOBILE_CARD_HEIGHT_ESTIMATE
    )
    return min(natural, Layout.MOBILE_MAX_COLUMN_HEIGHT)


def _build_column_content(page, col: ColumnModel, col_cards: List[CardModel], app):
    """Build the content for one column tab (header + cards + add button)."""
    # --- Header (compact for mobile)
    header = ft.Container(
        content=ft.Row(
            controls=[
                ft.Container(
                    width=4, height=20,
                    border_radius=2,
                    bgcolor=col.color,
                ),
                ft.Text(
                    col.title,
                    size=Typography.BODY_LG,
                    weight=ft.FontWeight.W_700,
                    color=Theme.TEXT_PRIMARY,
                ),
                ft.Container(
                    content=ft.Text(
                        str(len(col_cards)),
                        size=Typography.BODY_XS,
                        color=Theme.TEXT_SECONDARY,
                        weight=ft.FontWeight.W_600,
                    ),
                    bgcolor=Theme.BG_INPUT,
                    border_radius=Radius.SM,
                    padding=ft.Padding.symmetric(horizontal=8, vertical=3),
                ),
                ft.Container(expand=True),
                ft.IconButton(
                    ft.Icons.EDIT_OUTLINED,
                    icon_color=Theme.TEXT_MUTED,
                    icon_size=Typography.ICON_SM,
                    tooltip="Renommer",
                    on_click=lambda e: app.on_edit_column(col),
                    style=ft.ButtonStyle(padding=6),
                ),
                ft.IconButton(
                    ft.Icons.DELETE_OUTLINE_ROUNDED,
                    icon_color=Theme.TEXT_MUTED,
                    icon_size=Typography.ICON_SM,
                    tooltip="Supprimer",
                    on_click=lambda e: page.run_task(app.on_delete_column, col.id),
                    style=ft.ButtonStyle(padding=6),
                ),
            ],
            spacing=Spacing.XS,
        ),
        padding=ft.Padding.only(left=Spacing.SM, right=4, top=Spacing.XS, bottom=Spacing.XS),
    )

    # --- Cards list (no drag on mobile)
    # Height is dynamic: grows with card count, capped at MAX.
    # When cards exceed the height, the list scrolls vertically.
    cards_list_height = _calc_mobile_cards_list_height(len(col_cards))

    card_controls = []
    for c in col_cards:
        tc = TaskCard(
            page, c, app,
            app.on_edit_card, app.on_delete_card,
            col.color,
        )
        card_controls.append(tc)

    cards_list = ft.Column(
        controls=card_controls,
        spacing=Spacing.XS,
        scroll=ft.ScrollMode.AUTO,
        expand=False,  # Fixed height, not expand
        height=cards_list_height,
    )

    # --- Empty state
    if not col_cards:
        cards_list = ft.Column(
            controls=[
                ft.Container(height=Spacing.LG),
                ft.Icon(ft.Icons.INBOX_OUTLINED,
                        color=Theme.TEXT_MUTED, size=48),
                ft.Text("Aucune tache",
                        color=Theme.TEXT_SECONDARY, size=Typography.BODY),
                ft.Text("Ajoutez une tache pour commencer.",
                        color=Theme.TEXT_MUTED, size=Typography.BODY_SM),
            ],
            horizontal_alignment=ft.CrossAxisAlignment.CENTER,
            spacing=Spacing.XS,
            scroll=ft.ScrollMode.AUTO,
            expand=False,
            height=cards_list_height,
        )

    # --- Add task button
    add_btn = ft.Container(
        content=ft.Row(
            controls=[
                ft.Icon(ft.Icons.ADD_ROUNDED, color=Theme.TEXT_MUTED, size=Typography.ICON_SM),
                ft.Text("Ajouter une tache",
                        color=Theme.TEXT_SECONDARY,
                        weight=ft.FontWeight.W_500,
                        size=Typography.BODY_SM),
            ],
            spacing=Spacing.XS,
        ),
        border_radius=Radius.MD,
        padding=ft.Padding.symmetric(horizontal=Spacing.SM, vertical=12),
        on_click=lambda e: app.open_add_card_dialog(col.id),
        animate=ft.Animation(Duration.FAST, Easing.OUT),
    )

    # The whole tab content scrolls vertically if needed (header + cards + button).
    return ft.Container(
        content=ft.Column(
            controls=[header, cards_list, add_btn],
            spacing=Spacing.XS,
            expand=True,
            scroll=ft.ScrollMode.AUTO,
        ),
        bgcolor=Theme.BG_GLOBAL,
        padding=ft.Padding.only(left=Spacing.SM, right=Spacing.SM, top=0, bottom=Spacing.SM),
        expand=True,
    )
