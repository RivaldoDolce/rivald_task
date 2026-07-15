import flet as ft
from ...config import Theme, Layout, Spacing, Radius, Duration, Easing, Typography


def CustomTitleBar(page, on_toggle_sidebar, sidebar_open: bool,
                   unread_count: int = 0, on_notifications=None):
    """
    Title bar — logo first, then sidebar toggle, then notifications on the right.
    The notification bell shows an unread count badge and is functional.
    """
    async def close_app(e):
        await page.window.destroy()

    def minimize_app(e):
        page.window.minimized = True

    def maximize_app(e):
        page.window.maximized = not page.window.maximized

    # --- Logo block (always first)
    logo = ft.Row(
        controls=[
            ft.Container(
                content=ft.Icon(
                    ft.Icons.WIDGETS_ROUNDED,
                    color=Theme.NEON_BLUE,
                    size=Typography.ICON_LG,
                ),
                bgcolor=Theme.NEON_BLUE + "1A",
                border_radius=Radius.MD,
                padding=Spacing.XS,
            ),
            ft.Text(
                "Rivald",
                size=Typography.H4,
                weight=ft.FontWeight.W_700,
                color=Theme.TEXT_PRIMARY,
            ),
            ft.Text(
                "Task",
                size=Typography.H4,
                weight=ft.FontWeight.W_300,
                color=Theme.NEON_BLUE,
            ),
            ft.Container(
                content=ft.Text(
                    "PRO",
                    size=Typography.BODY_XS,
                    color=Theme.BG_GLOBAL,
                    weight=ft.FontWeight.W_800,
                ),
                bgcolor=Theme.NEON_BLUE,
                border_radius=3,
                padding=ft.Padding.symmetric(horizontal=6, vertical=2),
                margin=ft.Margin.only(left=4),
            ),
        ],
        spacing=Spacing.XS,
    )

    # --- Sidebar toggle (placed AFTER the title)
    toggle_btn = ft.IconButton(
        ft.Icons.MENU_OPEN_ROUNDED if sidebar_open else ft.Icons.MENU_ROUNDED,
        icon_color=Theme.TEXT_SECONDARY,
        icon_size=Typography.ICON_LG,
        on_click=on_toggle_sidebar,
        tooltip="Afficher / masquer la sidebar",
        style=ft.ButtonStyle(
            padding=ft.Padding.symmetric(horizontal=10, vertical=10),
        ),
    )

    # --- Notification bell
    # Using a clickable Container (not ft.Stack) so clicks always register.
    # The badge is a small Container positioned in the top-right corner.
    bell_icon = ft.Icon(
        ft.Icons.NOTIFICATIONS_ROUNDED if unread_count > 0
        else ft.Icons.NOTIFICATIONS_NONE_ROUNDED,
        color=Theme.NEON_BLUE if unread_count > 0 else Theme.TEXT_SECONDARY,
        size=Typography.ICON_LG,
    )

    if unread_count > 0:
        badge = ft.Container(
            content=ft.Text(
                str(min(unread_count, 99)),
                size=10,
                color=Theme.BG_GLOBAL,
                weight=ft.FontWeight.W_800,
                text_align=ft.TextAlign.CENTER,
            ),
            width=18,
            height=18,
            border_radius=9,
            bgcolor=Theme.NEON_RED,
            border=ft.Border.all(2, Theme.BG_GLOBAL),
            alignment=ft.Alignment(0, 0),
            right=-2,
            top=-2,
        )
        bell = ft.Stack(
            controls=[
                ft.Container(
                    content=bell_icon,
                    width=40,
                    height=40,
                    border_radius=Radius.MD,
                    on_click=on_notifications,
                    on_hover=lambda e: None,
                    alignment=ft.Alignment(0, 0),
                ),
                badge,
            ],
            width=40,
            height=40,
        )
        # Wrap the Stack in a Container with on_click as a fallback.
        bell_wrapper = ft.Container(
            content=bell,
            on_click=on_notifications,
            tooltip="Notifications",
            width=44,
            height=44,
            padding=2,
            alignment=ft.Alignment(0, 0),
        )
    else:
        bell_wrapper = ft.IconButton(
            ft.Icons.NOTIFICATIONS_NONE_ROUNDED,
            icon_color=Theme.TEXT_SECONDARY,
            icon_size=Typography.ICON_LG,
            on_click=on_notifications,
            tooltip="Notifications",
            style=ft.ButtonStyle(padding=10),
        )

    # --- Window controls
    window_controls = ft.Row(
        controls=[
            ft.IconButton(
                ft.Icons.MINIMIZE_ROUNDED,
                icon_color=Theme.TEXT_SECONDARY,
                icon_size=Typography.ICON,
                on_click=minimize_app,
                style=ft.ButtonStyle(padding=8),
            ),
            ft.IconButton(
                ft.Icons.CROP_SQUARE_ROUNDED,
                icon_color=Theme.TEXT_SECONDARY,
                icon_size=Typography.ICON,
                on_click=maximize_app,
                style=ft.ButtonStyle(padding=8),
            ),
            ft.IconButton(
                ft.Icons.CLOSE_ROUNDED,
                icon_color=Theme.NEON_RED,
                icon_size=Typography.ICON,
                on_click=close_app,
                style=ft.ButtonStyle(padding=8),
            ),
        ],
        spacing=0,
    )

    # --- Right side: bell + avatar + separator + window controls
    right_actions = ft.Row(
        controls=[
            bell_wrapper,
            ft.Container(
                content=ft.Text(
                    "U",
                    size=Typography.BODY_SM,
                    color=Theme.TEXT_PRIMARY,
                    weight=ft.FontWeight.W_700,
                ),
                width=32, height=32,
                border_radius=Radius.MD,
                bgcolor=Theme.NEON_PURPLE + "33",
                alignment=ft.Alignment(0, 0),
                tooltip="Profil utilisateur",
            ),
            ft.Container(width=1, height=24, bgcolor=Theme.BORDER_SUBTLE),
            window_controls,
        ],
        spacing=Spacing.XS,
    )

    return ft.WindowDragArea(
        ft.Container(
            content=ft.Row(
                controls=[
                    ft.Row(
                        controls=[logo, toggle_btn],
                        spacing=Spacing.SM,
                    ),
                    right_actions,
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            bgcolor=Theme.BG_GLOBAL,
            padding=ft.Padding.only(left=Spacing.SM, right=Spacing.XS, top=8, bottom=8),
            border=ft.Border.only(bottom=ft.BorderSide(1, Theme.BORDER_SUBTLE)),
            height=Layout.HEADER_HEIGHT,
        ),
        maximizable=True,
    )
