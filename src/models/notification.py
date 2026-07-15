from dataclasses import dataclass, field
from typing import Optional

@dataclass
class NotificationModel:
    """
    Une notification utilisateur.

    Types de notifications gérés :
    - card_created   : une carte a été créée
    - card_moved     : une carte a été déplacée entre colonnes
    - card_updated   : une carte a été modifiée
    - card_deleted   : une carte a été supprimée
    - card_overdue   : une carte a dépassé son échéance (au chargement)
    - column_created : une colonne a été créée
    - column_deleted : une colonne a été supprimée

    Priorités :
    - info     : information neutre (création, modification)
    - warning  : attention (échéance dépassée, suppression)
    - success  : action réussie (déplacement terminé)
    """
    id: Optional[int] = None
    type: str = "info"
    priority: str = "info"      # info | warning | success
    title: str = ""
    message: str = ""
    icon: str = "info"
    read: bool = False
    created_at: str = ""

    @property
    def color(self):
        return {
            "info": "#5B9CFF",
            "warning": "#F87171",
            "success": "#34D399",
        }.get(self.priority, "#94A3B8")
