import flet as ft
from typing import List
from ...config import Theme, Layout, Spacing, Radius, Duration, Easing, Typography
from ...models import ColumnModel, CardModel
from .task_card import TaskCard


# ============================================================================
#  COLUMN HEIGHT TUNING
#  ============================================================================
#  If the initial column height doesn't suit you, change MIN_COLUMN_HEIGHT
#  below. The column will never be shorter than this value (in pixels).
#
#  CARD_HEIGHT_ESTIMATE is the approximate height of one card in pixels.
#  The column grows by this amount for each additional card.
#
#  File: src/ui/kanban/kanban_column.py
#  ============================================================================
MIN_COLUMN_HEIGHT = 420
CARD_HEIGHT_ESTIMATE = 130
HEADER_HEIGHT = 56
ADD_BTN_HEIGHT = 48
COLUMN_PADDING = 24


class KanbanColumn(ft.Container):
    """
    A single Kanban column.

    Extends ft.Container (NOT ft.DragTarget) so that on mobile we can skip
    drag & drop entirely. The Flet 0.85.3 Android client sends DragTarget
    events without local_position/global_position, which crashes the event
    parser. Drag wrapping is applied externally in board_view.py on desktop.

    Behavior:
    - Minimum height enforced via MIN_COLUMN_HEIGHT (see constant above).
    - Grows with the number of cards (estimated per-card height).
    - Collapse/expand button toggles between showing all cards and header only.
    - Direct edit/delete icons in the top-right corner (no popup menu).
    - Halo only on hover/drag/selection.
    - Vertical color bar (4px) shows the column's status color.
    """

    WIDTH = Layout.COLUMN_WIDTH_DESKTOP

    def __init__(self, page, col: ColumnModel, all_cards: List[CardModel], app,
                 enable_drag: bool = True):
        super().__init__()
        self._page = page
        self.col = col
        self.all_cards = all_cards
        self.app = app
        self.enable_drag = enable_drag
        self.is_hovered = False
        self.is_selected = False
        self.is_collapsed = False
        self._refresh()

    # ------------------------------------------------------------------ helpers
    def _calc_height(self, num_cards: int) -> float:
        """Calculate the column height based on card count."""
        if self.is_collapsed:
            return HEADER_HEIGHT + COLUMN_PADDING
        content_height = (
            HEADER_HEIGHT
            + 1  # divider
            + max(1, num_cards) * CARD_HEIGHT_ESTIMATE
            + ADD_BTN_HEIGHT
            + COLUMN_PADDING
        )
        return max(MIN_COLUMN_HEIGHT, content_height)

    def _column_shadow(self):
        if self.is_hovered:
            return [
                ft.BoxShadow(
                    spread_radius=0, blur_radius=24,
                    color=self.col.color + "33", offset=ft.Offset(0, 0),
                ),
                Theme.SHADOW_COLUMN_HOVER,
            ]
        return [Theme.SHADOW_COLUMN]

    def _column_border(self):
        if self.is_hovered:
            return ft.Border.all(1, self.col.color + "66")
        if self.is_selected:
            return ft.Border.all(1, self.col.color + "44")
        return ft.Border.all(1, Theme.BORDER_SUBTLE)

    def _toggle_collapse(self, e=None):
        self.is_collapsed = not self.is_collapsed
        self._refresh()
        self.update()

    def _refresh(self):
        """Rebuild inner content and apply container-level properties."""
        self.content = self._build_inner()
        self._apply_props()

    def _apply_props(self):
        col_cards = [c for c in self.all_cards if c.column_id == self.col.id]
        self.width = self.WIDTH
        self.bgcolor = Theme.BG_COLUMN
        self.border_radius = Radius.LG
        self.border = self._column_border()
        self.shadow = self._column_shadow()
        self.animate = ft.Animation(Duration.NORMAL, Easing.OUT)
        self.alignment = ft.Alignment(0, -1)
        self.padding = ft.Padding.only(
            left=Spacing.SM,
            right=Spacing.SM,
            top=0,
            bottom=Spacing.SM,
        )
        self.height = self._calc_height(len(col_cards))

    # ------------------------------------------------------------------ build
    def _build_inner(self):
        col_cards = [c for c in self.all_cards if c.column_id == self.col.id]

        def open_add_card_dlg(e):
            self.app.open_add_card_dialog(self.col.id)

        # --- Direct edit / delete icons
        edit_btn = ft.IconButton(
            ft.Icons.EDIT_OUTLINED,
            icon_color=Theme.TEXT_MUTED,
            icon_size=Typography.ICON_SM,
            tooltip="Renommer la colonne",
            on_click=lambda e: self.app.on_edit_column(self.col),
            style=ft.ButtonStyle(padding=6),
        )
        delete_btn = ft.IconButton(
            ft.Icons.DELETE_OUTLINE_ROUNDED,
            icon_color=Theme.TEXT_MUTED,
            icon_size=Typography.ICON_SM,
            tooltip="Supprimer la colonne",
            on_click=lambda e: self._page.run_task(self.app.on_delete_column, self.col.id),
            style=ft.ButtonStyle(padding=6),
        )
        collapse_btn = ft.IconButton(
            ft.Icons.UNFOLD_LESS_ROUNDED if not self.is_collapsed
            else ft.Icons.UNFOLD_MORE_ROUNDED,
            icon_color=Theme.TEXT_MUTED,
            icon_size=Typography.ICON_SM,
            tooltip="Réduire / agrandir" if not self.is_collapsed else "Agrandir",
            on_click=self._toggle_collapse,
            style=ft.ButtonStyle(padding=6),
        )

        # --- Header
        header = ft.Container(
            content=ft.Row(
                controls=[
                    ft.Row(
                        controls=[
                            ft.Container(
                                width=4,
                                height=24,
                                border_radius=2,
                                bgcolor=self.col.color,
                            ),
                            ft.Text(
                                self.col.title,
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
                        ],
                        spacing=Spacing.XS,
                    ),
                    ft.Row(
                        controls=[collapse_btn, edit_btn, delete_btn],
                        spacing=0,
                    ),
                ],
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            padding=ft.Padding.only(left=Spacing.SM, right=4, top=Spacing.SM, bottom=12),
        )

        # --- Cards list
        if self.is_collapsed:
            cards_section = ft.Container(
                content=ft.Text(
                    f"{len(col_cards)} carte(s) — colonne réduite",
                    size=Typography.BODY_XS,
                    color=Theme.TEXT_MUTED,
                    italic=True,
                ),
                padding=ft.Padding.only(left=Spacing.SM, bottom=Spacing.SM),
            )
        else:
            card_controls = []
            for c in col_cards:
                tc = TaskCard(
                    self._page, c, self.app,
                    self.app.on_edit_card, self.app.on_delete_card,
                    self.col.color,
                )
                if self.enable_drag:
                    # Wrap card in Draggable for drag & drop (desktop only).
                    # NOTE: Flet 0.85.3 uses on_drag_complete (not on_drag_end).
                    card_controls.append(ft.Draggable(
                        group="kanban",
                        data=str(c.id),
                        content=tc,
                        on_drag_start=lambda e, cid=c.id: _set_attr(self.app, 'dragged_card_id', cid),
                        on_drag_complete=lambda e: _set_attr(self.app, 'dragged_card_id', None),
                    ))
                else:
                    card_controls.append(tc)

            cards_section = ft.Column(
                controls=card_controls,
                spacing=Spacing.XS,
                expand=False,
            )

        # --- Add task button
        if not self.is_collapsed:
            add_task_btn = ft.Container(
                content=ft.Row(
                    controls=[
                        ft.Icon(
                            ft.Icons.ADD_ROUNDED,
                            color=Theme.TEXT_MUTED,
                            size=Typography.ICON_SM,
                        ),
                        ft.Text(
                            "Ajouter une tâche",
                            color=Theme.TEXT_SECONDARY,
                            weight=ft.FontWeight.W_500,
                            size=Typography.BODY_SM,
                        ),
                    ],
                    spacing=Spacing.XS,
                ),
                border_radius=Radius.MD,
                padding=ft.Padding.symmetric(horizontal=Spacing.SM, vertical=12),
                on_click=open_add_card_dlg,
                on_hover=self._add_btn_hover,
                animate=ft.Animation(Duration.FAST, Easing.OUT),
            )
        else:
            add_task_btn = ft.Container()

        # Assemble inner Column
        controls = [header]
        if not self.is_collapsed:
            controls.append(ft.Divider(color=Theme.BORDER_SUBTLE, height=1))
        controls.append(cards_section)
        if not self.is_collapsed:
            controls.append(add_task_btn)

        return ft.Column(
            controls=controls,
            spacing=0,
            expand=False,
        )

    def _add_btn_hover(self, e):
        is_hover = e.data == "true"
        try:
            inner = self.content
            btn = inner.controls[-1]
            btn.bgcolor = Theme.BG_ELEVATED if is_hover else None
            btn.update()
        except Exception:
            pass

    # ------------------------------------------------------------------ drag target compat
    # These methods exist so board_view.py can optionally attach drag handlers.
    # They are no-ops unless the column is wrapped in a DragTarget externally.
    def set_hovered(self, hovered: bool):
        self.is_hovered = hovered
        self._refresh()
        self.update()


def _set_attr(obj, attr, value):
    """Helper to set an attribute on an object."""
    setattr(obj, attr, value)
