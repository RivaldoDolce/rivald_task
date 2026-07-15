"""
Responsive breakpoints and layout routing.

The app selects a layout family based on `page.width`:
  - MOBILE   : width < 700  -> single-column, Tabs-based Kanban, drawer sidebar
  - TABLET   : 700 <= width < 1200 -> desktop layout with narrower sidebar
  - DESKTOP  : width >= 1200 -> full desktop layout

The router in `app.py` calls `select_layout(state)` to decide which family
to render, then instantiates the corresponding view module.
"""
from enum import Enum


class LayoutFamily(str, Enum):
    MOBILE = "mobile"
    TABLET = "tablet"
    DESKTOP = "desktop"


# Breakpoints (in pixels).
MOBILE_BREAKPOINT = 700
TABLET_BREAKPOINT = 1200


def select_layout(page_width: float) -> LayoutFamily:
    """Return the layout family for the given page width."""
    if page_width < MOBILE_BREAKPOINT:
        return LayoutFamily.MOBILE
    if page_width < TABLET_BREAKPOINT:
        return LayoutFamily.TABLET
    return LayoutFamily.DESKTOP


def is_mobile(page_width: float) -> bool:
    return page_width < MOBILE_BREAKPOINT


def is_tablet(page_width: float) -> bool:
    return MOBILE_BREAKPOINT <= page_width < TABLET_BREAKPOINT


def is_desktop(page_width: float) -> bool:
    return page_width >= TABLET_BREAKPOINT
