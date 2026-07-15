import flet as ft
from ...config import (
    Theme, LABEL_COLORS, Layout, Spacing, Radius, Duration, Easing, Typography,
)
from ...models import AppState
from ..components import PrimaryButton


def Sidebar(page, state: AppState, on_filter_change, on_view_change,
            on_add_column, on_search_query_change):
    """
    Sidebar with search, views, priority filters and color tags.
    - Click a color tag once to filter, click again to clear the filter.
    - Search field updates the main view without losing focus
      (handled at the app level: on_search_query_change only refreshes the
      BoardView, never the sidebar).
    """

    def set_priority_filter(p):
        # Click the active priority again to deselect.
        if state.filter_priority == p:
            state.filter_priority = None
        else:
            state.filter_priority = p
        on_filter_change()

    def set_color_filter(c):
        # Click the active color again to deselect — fixes the
        # "stuck filter" issue reported by the user.
        if state.filter_color == c:
            state.filter_color = None
        else:
            state.filter_color = c
        on_filter_change()

    # ------------------------------------------------------------------ helpers
    def nav_item(icon, label, color, is_active, on_click):
        return ft.Container(
            content=ft.Row(
                controls=[
                    ft.Icon(icon, color=color if is_active else Theme.TEXT_MUTED,
                            size=Typography.ICON),
                    ft.Text(
                        label,
                        size=Typography.BODY,
                        color=Theme.TEXT_PRIMARY if is_active else Theme.TEXT_SECONDARY,
                        weight=ft.FontWeight.W_600 if is_active else ft.FontWeight.W_400,
                    ),
                ],
                spacing=Spacing.XS,
            ),
            bgcolor=Theme.BG_ELEVATED if is_active else None,
            border_radius=Radius.MD,
            padding=ft.Padding.symmetric(horizontal=Spacing.SM, vertical=12),
            border=ft.Border.all(
                1, color + "55" if is_active else "transparent"
            ),
            on_click=on_click,
            animate=ft.Animation(Duration.FAST, Easing.OUT),
        )

    def filter_item(icon, label, color, is_active, on_click):
        return ft.Container(
            content=ft.Row(
                controls=[
                    (ft.Icon(icon, color=color, size=Typography.ICON_SM)
                     if icon else ft.Container(width=14, height=14,
                                               border_radius=4, bgcolor=color)),
                    ft.Text(
                        label,
                        size=Typography.BODY_SM,
                        color=Theme.TEXT_PRIMARY if is_active else Theme.TEXT_SECONDARY,
                        weight=ft.FontWeight.W_500 if is_active else ft.FontWeight.W_400,
                    ),
                ],
                spacing=Spacing.XS,
            ),
            bgcolor=Theme.BG_ELEVATED if is_active else None,
            border_radius=Radius.MD,
            padding=ft.Padding.symmetric(horizontal=Spacing.SM, vertical=10),
            on_click=on_click,
            animate=ft.Animation(Duration.FAST, Easing.OUT),
        )

    def section_label(text):
        return ft.Text(
            text.upper(),
            size=Typography.LABEL,
            color=Theme.TEXT_MUTED,
            weight=ft.FontWeight.W_700,
        )

    # ------------------------------------------------------------------ sections
    priority_options = [
        (None, ("Tous", Theme.TEXT_MUTED)),
        (4, ("Critique", Theme.NEON_RED)),
        (3, ("Haute", Theme.NEON_ORANGE)),
        (2, ("Moyenne", Theme.NEON_BLUE)),
        (1, ("Basse", Theme.NEON_GREEN)),
    ]

    priority_filters = ft.Column(
        controls=[
            section_label("Priorité"),
            ft.Column(
                controls=[
                    filter_item(
                        ft.Icons.FILTER_ALT_OUTLINED, label, color,
                        state.filter_priority == p,
                        lambda e, p=p: set_priority_filter(p),
                    )
                    for p, (label, color) in priority_options
                ],
                spacing=4,
            ),
        ],
        spacing=Spacing.XS,
    )

    color_filters = ft.Column(
        controls=[
            section_label("Étiquettes"),
            ft.Row(
                controls=[
                    ft.Container(
                        content=ft.Container(
                            width=24, height=24,
                            border_radius=6, bgcolor=color,
                        ),
                        padding=5,
                        border_radius=Radius.MD,
                        border=ft.Border.all(
                            2,
                            Theme.TEXT_PRIMARY
                            if state.filter_color == key
                            else "transparent",
                        ),
                        bgcolor=Theme.BG_ELEVATED
                        if state.filter_color == key
                        else None,
                        on_click=lambda e, k=key: set_color_filter(k),
                        tooltip=f"{label} — cliquer à nouveau pour annuler",
                        animate=ft.Animation(Duration.FAST, Easing.OUT),
                    )
                    for key, (label, color) in LABEL_COLORS.items() if color
                ],
                spacing=Spacing.XS,
                wrap=True,
            ),
            # Small helper text so users discover the "click again to clear" UX.
            ft.Text(
                "Astuce : cliquez à nouveau sur une étiquette pour annuler le filtre.",
                size=Typography.BODY_XS,
                color=Theme.TEXT_MUTED,
                italic=True,
            ),
        ],
        spacing=Spacing.XS,
    )

    nav_items = ft.Column(
        controls=[
            section_label("Vues"),
            ft.Column(
                controls=[
                    nav_item(
                        ft.Icons.DASHBOARD_ROUNDED, "Tableau",
                        Theme.NEON_BLUE, state.view_mode == "board",
                        lambda e: on_view_change("board"),
                    ),
                    nav_item(
                        ft.Icons.LIST_ALT_ROUNDED, "Liste",
                        Theme.NEON_PURPLE, state.view_mode == "list",
                        lambda e: on_view_change("list"),
                    ),
                    nav_item(
                        ft.Icons.INSIGHTS_ROUNDED, "Analytique",
                        Theme.NEON_GREEN, state.view_mode == "analytics",
                        lambda e: on_view_change("analytics"),
                    ),
                ],
                spacing=4,
            ),
        ],
        spacing=Spacing.XS,
    )

    # ------------------------------------------------------------------ layout
    # Search field is built ONCE per sidebar render; the app preserves
    # the sidebar reference across search changes, so focus is kept.
    search_field = ft.TextField(
        prefix_icon=ft.Icons.SEARCH_ROUNDED,
        hint_text="Rechercher une tâche...",
        hint_style=ft.TextStyle(color=Theme.TEXT_MUTED, size=Typography.BODY_SM),
        value=state.search_query,
        on_change=lambda e: on_search_query_change(e.control.value),
        bgcolor=Theme.BG_INPUT,
        border_color=Theme.BORDER_SUBTLE,
        focused_border_color=Theme.NEON_BLUE,
        color=Theme.TEXT_PRIMARY,
        border_radius=Radius.MD,
        text_size=Typography.BODY,
        height=44,
        content_padding=ft.Padding.symmetric(horizontal=Spacing.SM, vertical=0),
    )

    content = ft.Column(
        controls=[
            search_field,
            nav_items,
            priority_filters,
            color_filters,
            ft.Container(expand=True),
            PrimaryButton(
                "Nouvelle colonne",
                on_add_column,
                icon=ft.Icons.ADD_ROUNDED,
                expand=True,
            ),
        ],
        spacing=Spacing.MD,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )

    # Adaptive width: narrower on mobile (sidebar becomes overlay).
    width = Layout.SIDEBAR_WIDTH_MOBILE if state.is_mobile else Layout.SIDEBAR_WIDTH

    return ft.Container(
        content=content,
        width=width,
        bgcolor=Theme.BG_COLUMN,
        padding=ft.Padding.only(
            left=Spacing.SM,
            right=Spacing.SM,
            top=Spacing.SM,
            bottom=Spacing.SM,
        ),
        border=ft.Border.only(right=ft.BorderSide(1, Theme.BORDER_SUBTLE)),
    )
