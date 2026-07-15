import json
from dataclasses import dataclass
from datetime import datetime
from typing import Optional

@dataclass
class CardModel:
    id: int
    title: str
    description: str = ""
    color: str = "transparent"
    priority: int = 1
    tags: str = "[]"
    due_date: Optional[str] = None
    assignee: Optional[str] = None
    checklist: str = "[]"
    attachments: int = 0
    comments_count: int = 0
    column_id: int = 0
    created_at: str = ""
    updated_at: str = ""

    def get_tags_list(self):
        try:
            return json.loads(self.tags)
        except Exception:
            return []

    def is_overdue(self):
        if not self.due_date:
            return False
        try:
            due = datetime.strptime(self.due_date, "%Y-%m-%d")
            return due < datetime.now()
        except Exception:
            return False

    def days_until_due(self):
        if not self.due_date:
            return None
        try:
            due = datetime.strptime(self.due_date, "%Y-%m-%d")
            delta = (due - datetime.now()).days
            return delta
        except Exception:
            return None
