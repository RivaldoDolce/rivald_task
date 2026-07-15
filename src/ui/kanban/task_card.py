import flet as ft
from ...config import Theme, LABEL_COLORS, Spacing, Radius, Duration, Easing, Typography
from ...models import CardModel
from ..components.badges import PriorityBadge, TagChip, DueDateBadge


class TaskCard(ft.Container):
    """
    A single task card. Extends ft.Container (NOT ft.Draggable).
    Drag wrapping is applied by KanbanColumn on desktop only.
    On mobile, the card is a plain Container — avoids the Flet 0.85.3
    Android DragTargetEvent crash.
    """

    def __init__(self, page, card: CardModel, app, on_edit, on_delete,
                 col_color: str = Theme.BORDER_SUBTLE):
        super().__init__()
        self._page = page
        self.card = card
        self.app = app
        self.on_edit = on_edit
        self.on_delete = on_delete
        self.col_color = col_color
        self.is_hovered = False
        self.is_expanded = False
        self._refresh()

    # ------------------------------------------------------------------ events
    def handle_hover(self, e):
        self.is_hovered = e.data == "true"
        self._refresh()
        self.update()

    def toggle_expand(self, e):
        self.is_expanded = not self.is_expanded
        self._refresh()
        self.update()

    # ------------------------------------------------------------------ build
    def _refresh(self):
        """Rebuild inner content and apply container-level properties."""
        self.content = self._build_inner()
        self._apply_props()

    def _apply_props(self):
        dot_color = LABEL_COLORS.get(self.card.color, ("", None))[1]
        if not dot_color:
            dot_color = self.col_color
        border_color = Theme.BORDER_HOVER if self.is_hovered else Theme.BORDER_SUBTLE
        shadow = Theme.SHADOW_CARD_HOVER if self.is_hovered else Theme.SHADOW_CARD
        self.bgcolor = Theme.BG_CARD_HOVER if self.is_hovered else Theme.BG_CARD
        self.border_radius = Radius.MD
        self.padding = Spacing.SM
        self.border = ft.Border.all(1, border_color)
        self.shadow = shadow
        self.on_hover = self.handle_hover
        self.animate = ft.Animation(Duration.NORMAL, Easing.OUT)

    def _build_inner(self):
        tags = self.card.get_tags_list()
        overdue = self.card.is_overdue()

        edit_btn = ft.IconButton(
            ft.Icons.EDIT_OUTLINED,
            icon_color=Theme.TEXT_MUTED,
            icon_size=Typography.ICON_XS,
            tooltip="Modifier la carte",
            on_click=lambda e: self.on_edit(self.card),
            style=ft.ButtonStyle(padding=4),
        )
        delete_btn = ft.IconButton(
            ft.Icons.DELETE_OUTLINE_ROUNDED,
            icon_color=Theme.TEXT_MUTED,
            icon_size=Typography.ICON_XS,
            tooltip="Supprimer la carte",
            on_click=lambda e: self._page.run_task(self.on_delete, self.card.id),
            style=ft.ButtonStyle(padding=4),
        )
        expand_btn = ft.IconButton(
            ft.Icons.EXPAND_MORE_ROUNDED if not self.is_expanded
            else ft.Icons.EXPAND_LESS_ROUNDED,
            icon_color=Theme.TEXT_MUTED,
            icon_size=Typography.ICON_XS,
            tooltip="Voir plus / Voir moins",
            on_click=self.toggle_expand,
            style=ft.ButtonStyle(padding=4),
        )

        dot_color = LABEL_COLORS.get(self.card.color, ("", None))[1]
        if not dot_color:
            dot_color = self.col_color

        return ft.Column(
            controls=[
                ft.Row(
                    controls=[
                        ft.Container(
                            width=10, height=10,
                            border_radius=5,
                            bgcolor=dot_color,
                        ) if dot_color else ft.Container(width=10),
                        ft.Text(
                            self.card.title,
                            color=Theme.TEXT_PRIMARY,
                            weight=ft.FontWeight.W_600,
                            size=Typography.BODY_MD,
                            expand=True,
                        ),
                        expand_btn,
                        edit_btn,
                        delete_btn,
                    ],
                    alignment=ft.MainAxisAlignment.START,
                    spacing=4,
                ),
                ft.Container(
                    content=ft.Text(
                        self.card.description or "Aucune description",
                        color=Theme.TEXT_SECONDARY,
                        size=Typography.BODY_SM,
                        max_lines=3 if not self.is_expanded else None,
                        overflow=ft.TextOverflow.ELLIPSIS
                        if not self.is_expanded
                        else None,
                    ),
                    visible=bool(self.card.description) or self.is_expanded,
                ),
                ft.Row(
                    controls=[TagChip(t) for t in tags[:4]],
                    spacing=6,
                    wrap=True,
                    visible=len(tags) > 0,
                ),
                ft.Row(
                    controls=[
                        PriorityBadge(self.card.priority),
                        DueDateBadge(self.card.due_date, overdue),
                        ft.Container(
                            content=ft.Row(
                                controls=[
                                    ft.Icon(
                                        ft.Icons.PERSON_OUTLINE_ROUNDED,
                                        color=Theme.TEXT_MUTED,
                                        size=Typography.ICON_XS,
                                    ),
                                    ft.Text(
                                        self.card.assignee or "Non assigné",
                                        size=Typography.BODY_XS,
                                        color=Theme.TEXT_MUTED,
                                    ),
                                ],
                                spacing=4,
                            ),
                            visible=bool(self.card.assignee),
                        ),
                    ],
                    spacing=Spacing.XS,
                    wrap=True,
                ),
                ft.Divider(color=Theme.BORDER_SUBTLE, height=1)
                if self.is_expanded
                else ft.Container(),
                ft.Row(
                    controls=[
                        ft.Container(
                            content=ft.Row(
                                controls=[
                                    ft.Icon(
                                        ft.Icons.ATTACH_FILE_ROUNDED,
                                        color=Theme.TEXT_MUTED,
                                        size=Typography.ICON_XS,
                                    ),
                                    ft.Text(
                                        str(self.card.attachments),
                                        size=Typography.BODY_XS,
                                        color=Theme.TEXT_MUTED,
                                    ),
                                ],
                                spacing=2,
                            ),
                            visible=self.card.attachments > 0,
                        ),
                        ft.Container(
                            content=ft.Row(
                                controls=[
                                    ft.Icon(
                                        ft.Icons.CHAT_BUBBLE_OUTLINE_ROUNDED,
                                        color=Theme.TEXT_MUTED,
                                        size=Typography.ICON_XS,
                                    ),
                                    ft.Text(
                                        str(self.card.comments_count),
                                        size=Typography.BODY_XS,
                                        color=Theme.TEXT_MUTED,
                                    ),
                                ],
                                spacing=2,
                            ),
                            visible=self.card.comments_count > 0,
                        ),
                    ],
                    spacing=Spacing.SM,
                ),
            ],
            spacing=Spacing.XS,
        )
