import flet as ft
from .models import AppState, CardModel, ColumnModel, NotificationModel
from .database import (
    init_db, get_all_columns, get_all_cards, add_card as add_card_db,
    update_card_details as update_card_details_db, delete_card as delete_card_db,
    update_card_column as update_card_column_db, add_column as add_column_db,
    update_column_title as update_column_title_db, delete_column as delete_column_db,
    reorder_columns as reorder_columns_db,
    log_activity,
    get_all_notifications, add_notification, mark_all_read,
    clear_all_notifications,
)
from .ui.chrome import CustomTitleBar
from .ui.sidebar import Sidebar
from .ui.views import ListView, AnalyticsView
from .ui.kanban import BoardView
from .ui.mobile import MobileKanbanView, MobileAnalyticsView, MobileListView, MobileTitleBar
from .ui.responsive import LayoutFamily, select_layout, MOBILE_BREAKPOINT
from .ui.dialogs import CardEditDialog, AddCardDialog, AddColumnDialog, ColumnEditDialog


class RivaldTaskApp(ft.Column):
    def __init__(self, page: ft.Page):
        super().__init__()
        self._page = page
        self.state = AppState()
        self.expand = True
        self.view_container = ft.Container(expand=True)
        self.sidebar_container = ft.Container()
        self.title_bar_container = ft.Container()
        self.dragged_card_id = None
        self.dragged_column_id = None
        self._sidebar_ref = None
        # Mobile navigation drawer (created lazily).
        self._drawer = None

        self.controls = [
            self.title_bar_container,
            ft.Row([self.sidebar_container, self.view_container], expand=True)
        ]

        # Initial responsive state.
        try:
            self._page.on_resize = self._on_resize
        except Exception:
            pass

        try:
            self.state.page_width = float(self._page.width or 1920)
            family = select_layout(self.state.page_width)
            self.state.is_mobile = family == LayoutFamily.MOBILE
            if self.state.is_mobile:
                self.state.sidebar_open = False
        except Exception:
            pass

    @property
    def page(self):
        return self._page

    @property
    def current_layout(self) -> LayoutFamily:
        return select_layout(self.state.page_width)

    # ------------------------------------------------------------------ lifecycle
    async def init_and_load(self):
        await init_db()
        await self.load_data()
        await self.load_notifications()
        await self.notify_overdue_cards()

    async def load_data(self):
        cols_data = await get_all_columns()
        cards_data = await get_all_cards()

        self.state.columns = [
            ColumnModel(id=col['id'], title=col['title'], color=col['color'], position=col['position'])
            for col in cols_data
        ]
        self.state.all_cards = [
            CardModel(
                id=card['id'], title=card['title'], description=card['description'], color=card['color'],
                priority=card['priority'], tags=card['tags'], due_date=card['due_date'], assignee=card['assignee'],
                checklist=card['checklist'], attachments=card['attachments'], comments_count=card['comments_count'],
                column_id=card['column_id'], created_at=card['created_at'], updated_at=card['updated_at']
            ) for card in cards_data
        ]
        self.render_all()

    async def load_notifications(self):
        rows = await get_all_notifications()
        self.state.notifications = [
            NotificationModel(
                id=r['id'], type=r['type'], priority=r['priority'],
                title=r['title'], message=r['message'], icon=r['icon'],
                read=bool(r['read']), created_at=r['created_at'],
            )
            for r in rows
        ]

    async def notify_overdue_cards(self):
        """Auto-generate notifications for overdue cards (once per app launch)."""
        already_notified_titles = {n.title for n in self.state.notifications
                                    if n.type == 'card_overdue'}
        new_overdue = [
            c for c in self.state.all_cards
            if c.is_overdue() and f"Carte en retard : {c.title}" not in already_notified_titles
        ]
        for card in new_overdue:
            await add_notification(
                'card_overdue',
                f"Carte en retard : {card.title}",
                f"Échéance dépassée : {card.due_date}",
                priority='warning',
                icon='warning',
            )
        if new_overdue:
            await self.load_notifications()

    # ------------------------------------------------------------------ rendering
    def render_all(self):
        """Full re-render: title bar + sidebar/drawer + main view."""
        self.render_title_bar()
        self.render_main_view()
        self.render_sidebar(force_rebuild=True)
        if self.page:
            self.page.update()

    def render_main_view(self):
        filtered_cards = self.state.get_filtered_cards()
        family = self.current_layout

        if family == LayoutFamily.MOBILE:
            # Mobile views
            if self.state.view_mode == "board":
                self.view_container.content = MobileKanbanView(self.page, self.state, self)
            elif self.state.view_mode == "list":
                self.view_container.content = MobileListView(self.page, filtered_cards, self.on_edit_card, self.on_delete_card)
            elif self.state.view_mode == "analytics":
                self.view_container.content = MobileAnalyticsView(filtered_cards, self.state.columns)
        else:
            # Desktop / tablet views
            if self.state.view_mode == "board":
                self.view_container.content = BoardView(self.page, self.state, self)
            elif self.state.view_mode == "list":
                self.view_container.content = ListView(self.page, filtered_cards, self.on_edit_card, self.on_delete_card)
            elif self.state.view_mode == "analytics":
                self.view_container.content = AnalyticsView(filtered_cards, self.state.columns)

    def render_title_bar(self):
        family = self.current_layout
        if family == LayoutFamily.MOBILE:
            self.title_bar_container.content = MobileTitleBar(
                self.page, self.open_drawer,
                self.state.unread_count, self.toggle_notifications,
            )
        else:
            self.title_bar_container.content = CustomTitleBar(
                self.page, self.toggle_sidebar, self.state.sidebar_open,
                self.state.unread_count, self.toggle_notifications,
            )

    def render_sidebar(self, force_rebuild=False):
        """
        Desktop/tablet: render the sidebar inline.
        Mobile: sidebar is replaced by a navigation drawer (no inline sidebar).
        """
        family = self.current_layout
        if family == LayoutFamily.MOBILE:
            self.sidebar_container.content = ft.Container(width=0)
            self._sidebar_ref = None
            self._build_drawer()
            return

        if not self.state.sidebar_open:
            self.sidebar_container.content = ft.Container(width=0)
            self._sidebar_ref = None
            return

        if force_rebuild or self._sidebar_ref is None:
            self._sidebar_ref = Sidebar(
                self.page, self.state,
                self.on_filter_change, self.on_view_change,
                self.on_add_column, self.on_search_query_change,
            )
            self.sidebar_container.content = self._sidebar_ref

    def _build_drawer(self):
        """Build (or rebuild) the mobile navigation drawer."""
        from .config import Theme, Layout, Spacing, Radius, Typography
        from .ui.sidebar import Sidebar

        # The drawer content reuses the Sidebar component but with mobile width.
        self.state.is_mobile = True
        drawer_content = Sidebar(
            self.page, self.state,
            self.on_filter_change, self.on_view_change,
            self.on_add_column, self.on_search_query_change,
        )

        self._drawer = ft.NavigationDrawer(
            controls=[
                ft.Container(
                    content=ft.Row(
                        [
                            ft.Icon(ft.Icons.WIDGETS_ROUNDED, color=Theme.NEON_BLUE,
                                    size=Typography.ICON_LG),
                            ft.Text("RivaldTask", size=Typography.H4,
                                    weight=ft.FontWeight.W_700,
                                    color=Theme.TEXT_PRIMARY),
                        ],
                        spacing=Spacing.XS,
                    ),
                    padding=ft.Padding.only(left=Spacing.MD, top=Spacing.MD, bottom=Spacing.SM),
                ),
                ft.Divider(color=Theme.BORDER_SUBTLE),
                # The sidebar content is placed in a scrollable Column so it
                # works even on small screens with many filters.
                ft.Container(
                    content=drawer_content,
                    expand=True,
                ),
            ],
            bgcolor=Theme.BG_COLUMN,
            width=Layout.SIDEBAR_WIDTH_MOBILE,
        )

        # Attach the drawer to the page.
        # In Flet 0.85, the property is `page.drawer` (not `page.navigation_drawer`).
        try:
            self.page.drawer = self._drawer
        except Exception:
            try:
                # Fallback: append to overlay.
                self.page.overlay.append(self._drawer)
            except Exception:
                pass

    def open_drawer(self, e=None):
        """Open the mobile navigation drawer."""
        if self._drawer is None:
            self._build_drawer()
        try:
            # Flet 0.85: use page.show_drawer() to open the drawer.
            # This both registers the drawer on the page and opens it.
            self.page.show_drawer(self._drawer)
        except Exception:
            # Fallback: try setting open=True directly.
            try:
                if self._drawer not in self.page.overlay:
                    self.page.overlay.append(self._drawer)
                self._drawer.open = True
                self.page.update()
            except Exception:
                pass

    # ------------------------------------------------------------------ events
    def _on_resize(self, e):
        try:
            new_width = float(e.width)
        except Exception:
            new_width = float(self._page.width or 1920)
        old_family = self.current_layout
        self.state.page_width = new_width
        new_family = self.current_layout
        self.state.is_mobile = new_family == LayoutFamily.MOBILE

        # If the layout family changed (e.g. user rotated phone or resized window),
        # rebuild everything.
        if old_family != new_family:
            if new_family == LayoutFamily.MOBILE:
                self.state.sidebar_open = False
            else:
                self.state.sidebar_open = True
            self.render_all()
        else:
            # Same family — just update the page.
            if self.page:
                self.page.update()

    def on_search_query_change(self, query):
        """Update search filter without rebuilding the sidebar (preserves focus)."""
        self.state.search_query = query
        self.render_main_view()
        if self.page:
            self.page.update()

    def on_filter_change(self):
        """Filter changes need a main view refresh; sidebar is rebuilt to reflect state."""
        self.render_main_view()
        self.render_sidebar(force_rebuild=True)
        if self.page:
            self.page.update()

    def on_view_change(self, view_mode):
        self.state.view_mode = view_mode
        self.render_main_view()
        self.render_sidebar(force_rebuild=True)
        if self.page:
            self.page.update()
        # Close drawer if open (mobile UX: selecting a view closes the menu).
        if self._drawer is not None:
            try:
                self._drawer.open = False
                self.page.update()
            except Exception:
                pass

    def toggle_sidebar(self, e=None):
        self.state.sidebar_open = not self.state.sidebar_open
        self.render_title_bar()
        self.render_sidebar(force_rebuild=True)
        if self.page:
            self.page.update()

    # ------------------------------------------------------------------ notifications
    def toggle_notifications(self, e=None):
        """Open the notifications panel."""
        if self.state.notifications_open:
            return
        self.state.notifications_open = True
        panel = self._build_notifications_panel()
        # IMPORTANT: the panel must be assigned to self.page.overlay BEFORE
        # we set open=True, and we keep a reference so close_panel can find it.
        self.page.overlay.append(panel)
        panel.open = True
        self.page.update()

    def _build_notifications_panel(self):
        """
        Build the notifications AlertDialog.

        IMPORTANT: the AlertDialog is assigned to a local variable `panel`
        BEFORE the closures `close_panel` and `clear_all` are invoked at
        runtime. The closures capture `panel` by reference (Python closure
        semantics), so as long as `panel` is assigned in the enclosing scope
        before the closures are called, they will find it.

        The previous bug was that the function returned `ft.AlertDialog(...)`
        directly without assigning it to `panel`, so the closures raised
        NameError when invoked.
        """
        from .config import Theme, Spacing, Radius, Typography
        page = self.page

        # We declare `panel` as a list cell so the closures can mutate it
        # without requiring `nonlocal` (simpler and more robust).
        panel_holder = []

        async def close_panel(e=None):
            if panel_holder:
                panel_holder[0].open = False
            self.state.notifications_open = False
            try:
                await mark_all_read()
                await self.load_notifications()
            except Exception:
                pass
            self.render_title_bar()
            try:
                page.update()
            except Exception:
                pass

        async def clear_all(e=None):
            try:
                await clear_all_notifications()
                await self.load_notifications()
            except Exception:
                pass
            self.render_title_bar()
            if panel_holder:
                panel_holder[0].open = False
            self.state.notifications_open = False
            try:
                page.update()
            except Exception:
                pass

        # Build the notifications list
        items = []
        if not self.state.notifications:
            items.append(
                ft.Container(
                    content=ft.Column(
                        [
                            ft.Icon(ft.Icons.NOTIFICATIONS_NONE_ROUNDED,
                                    color=Theme.TEXT_MUTED, size=48),
                            ft.Text("Aucune notification",
                                    color=Theme.TEXT_SECONDARY, size=Typography.BODY),
                            ft.Text("Vos alertes apparaîtront ici.",
                                    color=Theme.TEXT_MUTED, size=Typography.BODY_SM),
                        ],
                        horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                        spacing=Spacing.XS,
                    ),
                    padding=Spacing.LG,
                    alignment=ft.Alignment(0, 0),
                )
            )
        else:
            for n in self.state.notifications:
                icon_map = {
                    "info": ft.Icons.INFO_OUTLINE_ROUNDED,
                    "warning": ft.Icons.WARNING_AMBER_ROUNDED,
                    "success": ft.Icons.CHECK_CIRCLE_OUTLINE_ROUNDED,
                }
                items.append(
                    ft.Container(
                        content=ft.Row(
                            [
                                ft.Container(
                                    content=ft.Icon(
                                        icon_map.get(n.icon, ft.Icons.INFO_OUTLINE_ROUNDED),
                                        color=n.color, size=Typography.ICON_LG,
                                    ),
                                    width=40, height=40,
                                    bgcolor=n.color + "1F",
                                    border_radius=Radius.MD,
                                    alignment=ft.Alignment(0, 0),
                                ),
                                ft.Column(
                                    [
                                        ft.Text(n.title, color=Theme.TEXT_PRIMARY,
                                                size=Typography.BODY,
                                                weight=ft.FontWeight.W_600),
                                        ft.Text(n.message, color=Theme.TEXT_SECONDARY,
                                                size=Typography.BODY_SM,
                                                max_lines=2,
                                                overflow=ft.TextOverflow.ELLIPSIS)
                                        if n.message else ft.Container(),
                                        ft.Text(self._format_timestamp(n.created_at),
                                                color=Theme.TEXT_MUTED,
                                                size=Typography.BODY_XS),
                                    ],
                                    spacing=2,
                                    expand=True,
                                ),
                                ft.Container(
                                    width=8, height=8, border_radius=4,
                                    bgcolor=n.color,
                                    visible=not n.read,
                                ),
                            ],
                            spacing=Spacing.SM,
                        ),
                        padding=Spacing.SM,
                        border_radius=Radius.MD,
                        bgcolor=Theme.BG_CARD if not n.read else None,
                        border=ft.Border.all(
                            1, Theme.BORDER_SUBTLE if not n.read else "transparent"
                        ),
                    )
                )

        # Width adapts to layout family.
        family = self.current_layout
        dialog_width = 360 if family == LayoutFamily.MOBILE else 480

        panel = ft.AlertDialog(
            modal=True,
            title=ft.Row(
                [
                    ft.Icon(ft.Icons.NOTIFICATIONS_NONE_ROUNDED,
                            color=Theme.NEON_BLUE, size=Typography.ICON_XL),
                    ft.Text("Notifications", color=Theme.TEXT_PRIMARY,
                            size=Typography.H3, weight=ft.FontWeight.W_700),
                    ft.Container(expand=True),
                    ft.TextButton(
                        "Tout effacer",
                        on_click=clear_all,
                        icon=ft.Icons.DELETE_SWEEP_ROUNDED,
                    ),
                ],
                spacing=Spacing.SM,
            ),
            content=ft.Container(
                content=ft.Column(
                    items,
                    spacing=Spacing.XS,
                    scroll=ft.ScrollMode.AUTO,
                    tight=True,
                ),
                width=dialog_width,
                height=min(480, max(280, len(items) * 80)),
                padding=Spacing.XS,
            ),
            actions=[
                ft.TextButton("Fermer", on_click=close_panel),
            ],
            bgcolor=Theme.BG_COLUMN,
            shape=ft.RoundedRectangleBorder(radius=Radius.XL),
            open=False,  # We set open=True after appending to overlay.
            on_dismiss=close_panel,
        )

        # Store the panel in the holder so the closures can find it.
        panel_holder.append(panel)
        return panel

    @staticmethod
    def _format_timestamp(ts):
        if not ts:
            return ""
        try:
            return ts.split('.')[0].replace('T', ' ')
        except Exception:
            return ts

    # ------------------------------------------------------------------ CRUD: cards
    async def add_card(self, column_id, title, description, color, priority, tags, due_date, assignee):
        card_id = await add_card_db(column_id, title, description, color, priority, tags, due_date, assignee)
        await self.load_data()
        await log_activity(card_id, "created", f"Carte '{title}' créée")
        col_title = next((c.title for c in self.state.columns if c.id == column_id), "?")
        await add_notification(
            'card_created',
            f"Nouvelle carte : {title}",
            f"Ajoutée à la colonne « {col_title} ».",
            priority='success', icon='success',
        )
        await self.load_notifications()
        self.render_title_bar()
        if self.page:
            self.page.update()

    async def update_card(self, card_id, title, desc, color, priority, tags, due_date, assignee):
        await update_card_details_db(card_id, title, desc, color, priority, tags, due_date, assignee)
        await self.load_data()
        await log_activity(card_id, "updated", f"Carte '{title}' modifiée")
        await add_notification(
            'card_updated',
            f"Carte modifiée : {title}",
            "Les détails ont été mis à jour.",
            priority='info', icon='info',
        )
        await self.load_notifications()
        self.render_title_bar()
        if self.page:
            self.page.update()

    async def on_delete_card(self, card_id):
        card = next((c for c in self.state.all_cards if c.id == card_id), None)
        title = card.title if card else f"#{card_id}"
        await delete_card_db(card_id)
        await self.load_data()
        await add_notification(
            'card_deleted',
            f"Carte supprimée : {title}",
            "La carte a été définitivement supprimée.",
            priority='warning', icon='warning',
        )
        await self.load_notifications()
        self.render_title_bar()
        if self.page:
            self.page.update()

    async def move_card(self, card_id, new_column_id):
        card = next((c for c in self.state.all_cards if c.id == card_id), None)
        old_col_id = card.column_id if card else None
        await update_card_column_db(card_id, new_column_id)
        await self.load_data()
        if card and old_col_id != new_column_id:
            col_title = next((c.title for c in self.state.columns if c.id == new_column_id), "?")
            await add_notification(
                'card_moved',
                f"Carte déplacée : {card.title}",
                f"Déplacée vers « {col_title} ».",
                priority='info', icon='info',
            )
            await self.load_notifications()
            self.render_title_bar()
            if self.page:
                self.page.update()

    # ------------------------------------------------------------------ CRUD: columns
    def on_edit_card(self, card):
        def close_dlg():
            dlg.open = False
            self.page.update()
        dlg = CardEditDialog(self.page, card, self.update_card, close_dlg)
        dlg.open = True
        self.page.update()

    def open_add_card_dialog(self, column_id):
        def close_dlg():
            dlg.open = False
            self.page.update()
        dlg = AddCardDialog(self.page, column_id, self.add_card, close_dlg)
        dlg.open = True
        self.page.update()

    def on_add_column(self, e):
        def close_dlg():
            dlg.open = False
            self.page.update()
        dlg = AddColumnDialog(self.page, self.add_column, close_dlg)
        dlg.open = True
        self.page.update()

    async def add_column(self, title, color):
        await add_column_db(title, color)
        await self.load_data()
        await add_notification(
            'column_created',
            f"Nouvelle colonne : {title}",
            "La colonne a été ajoutée au tableau.",
            priority='success', icon='success',
        )
        await self.load_notifications()
        self.render_title_bar()
        if self.page:
            self.page.update()

    def on_edit_column(self, col):
        def close_dlg():
            dlg.open = False
            self.page.update()

        async def save_column(col_id, title):
            await update_column_title_db(col_id, title)
            await self.load_data()

        dlg = ColumnEditDialog(self.page, col, save_column, close_dlg)
        dlg.open = True
        self.page.update()

    async def on_delete_column(self, col_id):
        col = next((c for c in self.state.columns if c.id == col_id), None)
        title = col.title if col else f"#{col_id}"
        await delete_column_db(col_id)
        await self.load_data()
        await add_notification(
            'column_deleted',
            f"Colonne supprimée : {title}",
            "La colonne et toutes ses cartes ont été supprimées.",
            priority='warning', icon='warning',
        )
        await self.load_notifications()
        self.render_title_bar()
        if self.page:
            self.page.update()

    async def reorder_columns(self, ordered_ids):
        """Persist the new column order after a drag-drop reorder (desktop only)."""
        await reorder_columns_db(ordered_ids)
        await self.load_data()
