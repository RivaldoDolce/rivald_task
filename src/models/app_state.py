from dataclasses import dataclass, field
from typing import Optional, List
from .card import CardModel
from .column import ColumnModel
from .notification import NotificationModel

@dataclass
class AppState:
    columns: List[ColumnModel] = field(default_factory=list)
    all_cards: List[CardModel] = field(default_factory=list)
    notifications: List[NotificationModel] = field(default_factory=list)
    search_query: str = ""
    filter_priority: Optional[int] = None
    filter_color: Optional[str] = None
    show_completed: bool = True
    selected_card: Optional[CardModel] = None
    sidebar_open: bool = True
    notifications_open: bool = False
    dark_mode: bool = True
    view_mode: str = "board"
    is_mobile: bool = False
    page_width: float = 1920.0

    def get_filtered_cards(self):
        filtered = self.all_cards
        if self.search_query:
            q = self.search_query.lower()
            filtered = [c for c in filtered if q in c.title.lower() or q in (c.description or "").lower()]
        if self.filter_priority is not None:
            filtered = [c for c in filtered if c.priority == self.filter_priority]
        if self.filter_color is not None:
            filtered = [c for c in filtered if c.color == self.filter_color]
        return filtered

    @property
    def unread_count(self):
        return sum(1 for n in self.notifications if not n.read)
