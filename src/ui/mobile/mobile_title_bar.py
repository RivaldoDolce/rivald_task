"""
Mobile title bar.

Compact header for small screens:
- Hamburger menu on the left (opens the navigation drawer).
- Logo centered.
- Notification bell on the right.
- Window controls hidden (mobile uses native chrome).
"""
import flet as ft
from ...config import Theme, Layout, Spacing, Radius, Duration, Easing, Typography


def MobileTitleBar(page, on_open_drawer, unread_count: int = 0,
                   on_notifications=None):
    """Build the mobile title bar."""

    # --- Hamburger menu button
    menu_btn = ft.IconButton(
        ft.Icons.MENU_ROUNDED,
        icon_color=Theme.TEXT_PRIMARY,
        icon_size=Typography.ICON_LG,
        on_click=on_open_drawer,
        tooltip="Menu",
        style=ft.ButtonStyle(padding=8),
    )

    # --- Logo (compact, no PRO badge)
    logo = ft.Row(
        controls=[
            ft.Container(
                content=ft.Icon(
                    ft.Icons.WIDGETS_ROUNDED,
                    color=Theme.NEON_BLUE,
                    size=Typography.ICON,
                ),
                bgcolor=Theme.NEON_BLUE + "1A",
                border_radius=Radius.SM,
                padding=4,
            ),
            ft.Text(
                "RivaldTask",
                size=Typography.BODY_LG,
                weight=ft.FontWeight.W_700,
                color=Theme.TEXT_PRIMARY,
            ),
        ],
        spacing=Spacing.XS,
    )

    # --- Notification bell
    if unread_count > 0:
        bell = ft.Stack(
            controls=[
                ft.IconButton(
                    ft.Icons.NOTIFICATIONS_ROUNDED,
                    icon_color=Theme.NEON_BLUE,
                    icon_size=Typography.ICON_LG,
                    on_click=on_notifications,
                    tooltip="Notifications",
                    style=ft.ButtonStyle(padding=8),
                ),
                ft.Container(
                    content=ft.Text(
                        str(min(unread_count, 99)),
                        size=9,
                        color=Theme.BG_GLOBAL,
                        weight=ft.FontWeight.W_800,
                        text_align=ft.TextAlign.CENTER,
                    ),
                    width=16, height=16,
                    border_radius=8,
                    bgcolor=Theme.NEON_RED,
                    border=ft.Border.all(2, Theme.BG_GLOBAL),
                    alignment=ft.Alignment(0, 0),
                    right=-2, top=-2,
                ),
            ],
            width=40, height=40,
        )
        bell_wrapper = ft.Container(
            content=bell,
            on_click=on_notifications,
            tooltip="Notifications",
            width=44, height=44,
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
            style=ft.ButtonStyle(padding=8),
        )

    return ft.Container(
        content=ft.Row(
            controls=[
                menu_btn,
                ft.Container(expand=True),
                logo,
                ft.Container(expand=True),
                bell_wrapper,
            ],
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
        ),
        bgcolor=Theme.BG_GLOBAL,
        padding=ft.Padding.only(left=Spacing.XS, right=Spacing.XS, top=8, bottom=8),
        border=ft.Border.only(bottom=ft.BorderSide(1, Theme.BORDER_SUBTLE)),
        height=52,
    )
