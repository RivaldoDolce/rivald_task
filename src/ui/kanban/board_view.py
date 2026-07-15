import flet as ft
from ...config import Theme, Layout, Spacing, Radius, Duration, Easing, Typography
from .kanban_column import KanbanColumn


def BoardView(page, app_state, app):
    """
    Kanban board.

    Layout:
    - 5 columns per row (wrap=True). Extra columns wrap to the next row.
    - Only vertical scrolling (no horizontal scroll).
    - On desktop: columns are draggable/reorderable AND cards can be dragged
      between columns via DragTarget/Draggable.
    - On mobile: columns are plain Containers (no drag) to avoid the
      Flet 0.85.3 Android DragTargetEvent crash.
    """
    filtered_cards = app_state.get_filtered_cards()
    is_mobile = app_state.is_mobile

    column_controls = []
    for col in app_state.columns:
        kc = KanbanColumn(
            page, col, filtered_cards, app,
            enable_drag=not is_mobile,
        )
        if is_mobile:
            column_controls.append(kc)
        else:
            column_controls.append(_make_column_draggable(kc, app, app_state))

    columns_row = ft.Row(
        controls=column_controls,
        spacing=Layout.COLUMN_GAP,
        run_spacing=Layout.COLUMN_GAP,
        wrap=True,
        expand=False,
    )

    scroll_column = ft.Column(
        controls=[columns_row],
        spacing=0,
        scroll=ft.ScrollMode.AUTO,
        expand=True,
    )

    return ft.Container(
        content=scroll_column,
        expand=True,
        bgcolor=Theme.BG_GLOBAL,
        padding=ft.Padding.only(
            left=Spacing.MD,
            right=Spacing.MD,
            top=Spacing.MD,
            bottom=Spacing.SM,
        ),
    )


def _make_column_draggable(kc, app, app_state):
    """
    Wrap a KanbanColumn for desktop drag & drop:
    - Outer DragTarget (group="kanban_column") handles column reordering.
    - Inner Draggable (group="kanban_column") makes the column draggable.
    - The KanbanColumn itself is also wrapped in a DragTarget (group="kanban")
      so cards can be dropped onto it.

    Layer structure:
      ColumnReorderDragTarget (group="kanban_column")
        └── ColumnDraggable (group="kanban_column")
              └── CardDropDragTarget (group="kanban")
                    └── KanbanColumn (ft.Container)
    """
    # --- Card drop target: accepts cards dragged onto this column.
    class CardDropDragTarget(ft.DragTarget):
        def __init__(self, kc, app):
            super().__init__(group="kanban", content=kc)
            self.kc = kc
            self.app = app
            self.on_accept = self._on_accept
            self.on_will_accept = self._on_will_accept
            self.on_leave = self._on_leave

        def _on_will_accept(self, e):
            if getattr(self.app, 'dragged_column_id', None) is not None:
                return
            try:
                is_target = e.data == "true"
            except Exception:
                is_target = True
            if is_target:
                self.kc.set_hovered(True)

        def _on_leave(self, e):
            if self.kc.is_hovered:
                self.kc.set_hovered(False)

        def _on_accept(self, e):
            self.kc.set_hovered(False)
            if self.app.dragged_card_id is not None:
                if getattr(self.app, 'dragged_column_id', None) is not None:
                    return
                self.app.page.run_task(
                    self.app.move_card,
                    self.app.dragged_card_id,
                    self.kc.col.id,
                )
                self.app.dragged_card_id = None

    # --- Column draggable: makes the whole column draggable for reordering.
    class ColumnDraggable(ft.Draggable):
        def __init__(self, kc, app):
            card_target = CardDropDragTarget(kc, app)
            super().__init__(
                group="kanban_column",
                data=str(kc.col.id),
                content=card_target,
            )
            self.kc = kc
            self.app = app
            self.on_drag_start = self._on_drag_start
            # NOTE: Flet 0.85.3 uses on_drag_complete (not on_drag_end).
            self.on_drag_complete = self._on_drag_complete

        def _on_drag_start(self, e):
            self.app.dragged_column_id = self.kc.col.id

        def _on_drag_complete(self, e):
            self.app.dragged_column_id = None

    # --- Column reorder target: accepts other columns being dropped here.
    class ColumnReorderDragTarget(ft.DragTarget):
        def __init__(self, kc, app, app_state):
            draggable = ColumnDraggable(kc, app)
            super().__init__(group="kanban_column", content=draggable)
            self.kc = kc
            self.app = app
            self.app_state = app_state
            self.on_accept = self._on_accept
            self.on_will_accept = self._on_will_accept
            self.on_leave = self._on_leave

        def _on_will_accept(self, e):
            try:
                is_target = e.data == "true"
            except Exception:
                is_target = True
            if is_target and self.app.dragged_column_id is not None:
                if self.app.dragged_column_id != self.kc.col.id:
                    self.kc.set_hovered(True)

        def _on_leave(self, e):
            if self.kc.is_hovered:
                self.kc.set_hovered(False)

        def _on_accept(self, e):
            self.kc.set_hovered(False)
            dragged_id = self.app.dragged_column_id
            if dragged_id is None or dragged_id == self.kc.col.id:
                return
            ordered = [c.id for c in self.app_state.columns]
            try:
                src_idx = ordered.index(dragged_id)
                dst_idx = ordered.index(self.kc.col.id)
            except ValueError:
                return
            ordered.insert(dst_idx, ordered.pop(src_idx))
            self.app.page.run_task(self.app.reorder_columns, ordered)

    return ColumnReorderDragTarget(kc, app, app_state)
