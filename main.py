import os
import sys
import flet as ft
from src.app import RivaldTaskApp
from src.config import Theme
from src.ui.responsive import select_layout, LayoutFamily


def _resolve_icon_path():
    """
    Resolve the absolute path to the app icon PNG.

    We try multiple locations to be robust against different CWDs and
    packaging scenarios (development vs. frozen executable).
    """
    script_dir = os.path.dirname(os.path.abspath(__file__))
    candidate_paths = [
        os.path.join(script_dir, "assets", "icon.png"),
        os.path.join(os.getcwd(), "assets", "icon.png"),
        # When packaged with PyInstaller, _MEIPASS points to the bundle root.
        os.path.join(getattr(sys, "_MEIPASS", ""), "assets", "icon.png"),
    ]
    for path in candidate_paths:
        if path and os.path.isfile(path):
            return os.path.abspath(path)
    return None


async def main(page: ft.Page):
    page.title = "RivaldTask Pro"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = Theme.BG_GLOBAL
    page.padding = 0

    # --- Detect platform / layout family ---
    try:
        page_width = float(page.width or 1920)
    except Exception:
        page_width = 1920.0
    family = select_layout(page_width)

    try:
        is_desktop_platform = (
            not page.web
            and page.platform in (
                ft.PagePlatform.WINDOWS,
                ft.PagePlatform.MACOS,
                ft.PagePlatform.LINUX,
            )
        )
    except Exception:
        is_desktop_platform = False

    # --- Desktop: app icon + frameless window ---
    if is_desktop_platform:
        # App icon — page.window.icon expects an absolute file path on disk.
        # This sets the window icon (visible in the title bar and Alt+Tab
        # switcher on Linux/GTK, Windows and macOS).
        #
        # NOTE about the taskbar icon on Linux/GNOME:
        # On GNOME-based distros (including Pop!_OS), the taskbar/dock icon
        # is determined by the .desktop file of the running process, NOT by
        # page.window.icon. When you run `python3 main.py`, the taskbar shows
        # the Python icon because the process is `python3`.
        #
        # To get a custom taskbar icon on Linux, you have two options:
        #   1. Build a standalone executable with `flet build` or PyInstaller,
        #      then create a .desktop file pointing to your icon.
        #   2. Install a .desktop file that associates the icon with the app.
        #
        # The code below sets the WINDOW icon (title bar + Alt+Tab), which is
        # the best we can do programmatically from Flet.
        icon_path = _resolve_icon_path()
        if icon_path:
            try:
                page.window.icon = icon_path
            except Exception:
                pass

        # Frameless window on desktop only.
        try:
            page.window.title_bar_hidden = True
            page.window.frameless = True
        except Exception:
            pass

    # --- Font ---
    try:
        page.fonts = {"Inter": "/assets/fonts/Inter-Regular.ttf"}
        page.theme = ft.Theme(font_family="Inter")
    except Exception:
        pass

    app = RivaldTaskApp(page)

    # On mobile, wrap the whole app in a SafeArea so it doesn't overlap
    # the status bar (top) and the navigation bar (bottom).
    if family == LayoutFamily.MOBILE:
        safe_app = ft.SafeArea(
            content=app,
            expand=True,
            maintain_bottom_view_padding=True,
            minimum_padding=ft.Padding.all(0),
        )
        page.add(safe_app)
    else:
        page.add(app)

    await app.init_and_load()


if __name__ == "__main__":
    # ft.run() replaces the deprecated ft.app() in Flet 0.80+.
    # assets_dir tells Flet to serve files from the assets/ directory.
    ft.run(main, assets_dir="assets")
