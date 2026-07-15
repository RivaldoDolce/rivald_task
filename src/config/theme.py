import flet as ft

# =============================================================================
#  Design tokens — Linear / Raycast / Notion / Arc inspired
#  8px grid, short durations, easeOutCubic curves.
# =============================================================================

class Spacing:
    """8px grid — only these values are allowed."""
    XS = 8
    SM = 16
    MD = 24
    LG = 32
    XL = 48

class Radius:
    SM = 6
    MD = 10
    LG = 14
    XL = 18

class Duration:
    FAST = 150
    NORMAL = 200
    SLOW = 250

class Easing:
    OUT = ft.AnimationCurve.EASE_OUT
    IN_OUT = ft.AnimationCurve.EASE_IN_OUT
    BOUNCE = ft.AnimationCurve.EASE_OUT_BACK

class Layout:
    # Column width adapts to viewport; defaults shown for desktop.
    COLUMN_WIDTH_DESKTOP = 300
    COLUMN_WIDTH_MOBILE = 320        # full-width on mobile
    COLUMN_GAP = 16
    COLUMNS_PER_ROW = 5              # requested by user
    SIDEBAR_WIDTH = 264              # wider for larger fonts
    SIDEBAR_WIDTH_MOBILE = 280
    HEADER_HEIGHT = 60               # taller for larger fonts
    HEADER_HEIGHT_MOBILE = 52        # compact mobile header
    BOARD_PADDING = Spacing.MD
    # Mobile column height tuning (used by MobileKanbanView).
    MOBILE_MIN_COLUMN_HEIGHT = 280   # min height of the cards list area
    MOBILE_CARD_HEIGHT_ESTIMATE = 110
    MOBILE_MAX_COLUMN_HEIGHT = 600   # cap to avoid filling the whole screen

class Typography:
    """
    Centralized font sizes (px). Bumped up from previous version
    so the whole app is comfortably readable on desktop and mobile.
    """
    # Body
    BODY_XS = 12
    BODY_SM = 13
    BODY = 14
    BODY_MD = 15
    BODY_LG = 16
    # Headers
    H4 = 18
    H3 = 20
    H2 = 24
    H1 = 28
    # Display
    DISPLAY = 32
    COUNTER = 40
    # Labels (uppercase sections)
    LABEL = 11
    LABEL_LG = 12
    # Icon sizes
    ICON_XS = 14
    ICON_SM = 16
    ICON = 18
    ICON_LG = 20
    ICON_XL = 24

class Theme:
    # --- Backgrounds (calibrated depth levels) ---
    BG_GLOBAL = "#0B0E14"
    BG_COLUMN = "#11151F"
    BG_CARD = "#161B27"
    BG_CARD_HOVER = "#1B2231"
    BG_ELEVATED = "#1A2030"
    BG_INPUT = "#0F131C"
    BG_OVERLAY = "#000000E6"

    # --- Accents (status colors — visible but discreet) ---
    NEON_BLUE = "#5B9CFF"
    NEON_PURPLE = "#A78BFA"
    NEON_PINK = "#F472B6"
    NEON_GREEN = "#34D399"
    NEON_ORANGE = "#FB923C"
    NEON_RED = "#F87171"
    NEON_YELLOW = "#FACC15"
    NEON_CYAN = "#22D3EE"

    # --- Gradients ---
    GRADIENT_PRIMARY = ["#5B9CFF", "#8B5CF6"]
    GRADIENT_SUCCESS = ["#34D399", "#22D3EE"]
    GRADIENT_DANGER = ["#F87171", "#FB923C"]

    # --- Text ---
    TEXT_PRIMARY = "#F1F5F9"
    TEXT_SECONDARY = "#94A3B8"
    TEXT_MUTED = "#64748B"
    TEXT_ACCENT = "#5B9CFF"

    # --- Borders ---
    BORDER_SUBTLE = "#1F2735"
    BORDER_HOVER = "#2B3548"
    BORDER_ACTIVE = "#3A4658"
    BORDER_GLOW = "#5B9CFF22"

    # --- Shadows ---
    SHADOW_CARD = ft.BoxShadow(
        spread_radius=0, blur_radius=8,
        color="#00000066", offset=ft.Offset(0, 2)
    )
    SHADOW_CARD_HOVER = ft.BoxShadow(
        spread_radius=0, blur_radius=18,
        color="#00000088", offset=ft.Offset(0, 6)
    )
    SHADOW_COLUMN = ft.BoxShadow(
        spread_radius=0, blur_radius=10,
        color="#00000055", offset=ft.Offset(0, 4)
    )
    SHADOW_COLUMN_HOVER = ft.BoxShadow(
        spread_radius=0, blur_radius=24,
        color="#00000088", offset=ft.Offset(0, 8)
    )
    SHADOW_GLOW_BLUE = ft.BoxShadow(
        spread_radius=0, blur_radius=20,
        color="#5B9CFF22", offset=ft.Offset(0, 0)
    )
    SHADOW_GLOW_PURPLE = ft.BoxShadow(
        spread_radius=0, blur_radius=20,
        color="#A78BFA22", offset=ft.Offset(0, 0)
    )
