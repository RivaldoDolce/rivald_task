# RivaldTask Pro

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://python.org)
[![Flet](https://img.shields.io/badge/Flet-0.85.3-blue.svg)](https://flet.dev)
[![License](https://img.shields.io/badge/License-Private-red.svg)](LICENSE)

Application de gestion de tâches Kanban multi-plateforme construite avec **Flet 0.85.3** et **Python**. Fonctionne nativement sur Linux, Windows, macOS, Android et web avec une interface adaptée à chaque type d'appareil.

> Documentation technique complète pour développeurs et contributeurs.

---

## Sommaire

- [Aperçu](#aperçu)
- [Fonctionnalités](#fonctionnalités)
- [Architecture responsive](#architecture-responsive)
- [Installation](#installation)
- [Lancement](#lancement)
- [Structure du projet](#structure-du-projet)
- [Modèle de données](#modèle-de-données)
- [Système de notifications](#système-de-notifications)
- [Persistance](#persistance)
- [Personnalisation](#personnalisation)
- [API de configuration](#api-de-configuration)
- [Déploiement mobile](#déploiement-mobile)
- [Dépannage](#dépannage)
- [Limites connues](#limites-connues)

---

## Aperçu

RivaldTask Pro est une application Kanban pensée pour le bureau comme pour le mobile. Contrairement aux approches qui tentent de rendre une interface desktop responsive, cette application implémente **trois familles de layouts distinctes** sélectionnées automatiquement selon la largeur de l'écran :

| Famille | Largeur | Disposition |
|---------|---------|-------------|
| `MOBILE` | < 700 px | Onglets, drawer, vues empilées |
| `TABLET` | 700–1200 px | Desktop avec sidebar rétrécie |
| `DESKTOP` | ≥ 1200 px | Grille 5 colonnes, drag & drop complet |

Chaque famille dispose de ses propres composants dans `src/ui/mobile/` et `src/ui/kanban/` (desktop). La logique métier et les données sont partagées.

---

## Fonctionnalités

### Tableau Kanban

- **Desktop** : grille de 5 colonnes par ligne, wrap automatique, scroll vertical uniquement, drag & drop des cartes entre colonnes, réordonnancement des colonnes par glisser-déposer.
- **Mobile** : interface à onglets (`TabBar` + `TabBarView`), une colonne par onglet, swipe horizontal entre les colonnes.
- Chaque colonne possède une hauteur minimale configurable et grandit avec le nombre de cartes.
- Bouton réduire/agrandir par colonne.
- Barre verticale colorée (4 px) indiquant le statut de la colonne.
- Icônes modifier/supprimer directement visibles (pas de menu contextuel).

### Cartes

- Titre, description, étiquettes couleur, priorité, échéance, assigné, pièces jointes, commentaires.
- Icônes modifier/supprimer/étendre toujours visibles.
- Survol élève la carte (desktop uniquement).

### Sidebar / Drawer

- **Desktop/Tablet** : sidebar fixe à gauche avec recherche, vues, filtres priorité, filtres étiquettes, bouton nouvelle colonne.
- **Mobile** : `NavigationDrawer` ouvert via le menu hamburger, contenu identique à la sidebar desktop.
- Re-cliquer sur un filtre actif le désactive (priorité comme étiquette).
- Le champ de recherche conserve le focus pendant la frappe.

### Notifications

- Cloche de notification dans la barre de titre avec badge de non-lus.
- Panneau modal listant les 50 dernières notifications.
- Bouton « Tout effacer » et bouton « Fermer » (marque tout comme lu).
- Notifications générées automatiquement pour : création, modification, suppression, déplacement de cartes ; création, suppression de colonnes ; cartes en retard.
- Persistance en base SQLite, table `notifications`.

### Vues alternatives

- **Vue liste** : tableau trié par priorité, actions directes en fin de ligne.
- **Vue analytique** : compteurs (total, en retard, assignées, étiquettes actives) + barres de progression par priorité et par colonne. Sur mobile, les compteurs sont empilés verticalement.

---

## Architecture responsive

Le routing est centralisé dans `src/ui/responsive.py` :

```python
from src.ui.responsive import select_layout, LayoutFamily

family = select_layout(page.width)
# family == LayoutFamily.MOBILE | TABLET | DESKTOP
```

La classe `RivaldTaskApp` dans `src/app.py` appelle `render_main_view()` et `render_title_bar()` qui sélectionnent les composants appropriés selon `current_layout` :

```python
def render_main_view(self):
    family = self.current_layout
    if family == LayoutFamily.MOBILE:
        # MobileKanbanView, MobileListView, MobileAnalyticsView
    else:
        # BoardView, ListView, AnalyticsView (desktop/tablet)
```

Le passage d'une famille à l'autre (par rotation d'écran ou redimensionnement de fenêtre) déclenche un `render_all()` complet. La transition est instantanée car les données sont en mémoire.

### Points de rupture

| Constante | Valeur | Description |
|-----------|--------|-------------|
| `MOBILE_BREAKPOINT` | 700 | En dessous = mobile |
| `TABLET_BREAKPOINT` | 1200 | 700–1200 = tablet, ≥1200 = desktop |

Pour modifier ces valeurs, éditez `src/ui/responsive.py`.

---

## Installation

### Prérequis

- Python 3.10 ou supérieur
- pip

### Étapes

```bash
git clone <repo-url>
cd rivald_task
python -m venv .venv
source .venv/bin/activate  # Linux/macOS
# ou: .venv\Scripts\activate  # Windows
pip install -r requirements.txt
```

### Dépendances système (Linux)

Sur Linux, Flet peut nécessiter les bibliothèques suivantes :

```bash
sudo apt install libglib2.0-0 libegl1 libgl1 libsecret-1-0
```

---

## Lancement

### Desktop (Linux/Windows/macOS)

```bash
python main.py
```

Au premier lancement, Flet télécharge le runtime client (~50 Mo). La base SQLite `rivald_task.db` est créée automatiquement avec 5 colonnes par défaut : Backlog, À faire, En cours, Revue, Terminé.

### Web

```bash
python main.py
# L'application s'ouvre dans le navigateur par défaut
```

### Android

```bash
flet run --android main.py
```

Scannez le QR code affiché dans le terminal avec l'application Flet sur votre téléphone.

> **Note** : le drag & drop est désactivé sur mobile (voir [Dépannage](#dépannage)).

---

## Structure du projet

```
rivald_task/
├── main.py                          # Point d'entrée Flet
├── requirements.txt                 # flet==0.85.3, aiosqlite
├── assets/
│   ├── icon.svg                     # Icône vectorielle (source)
│   ├── icon.png                     # Icône raster 256x256 RGBA
│   └── fonts/
│       └── Inter-Regular.ttf        # Police Inter
├── src/
│   ├── app.py                       # Classe principale RivaldTaskApp
│   ├── config/
│   │   ├── theme.py                 # Design tokens (couleurs, espacements, typo)
│   │   ├── labels.py                # Mappage étiquettes / couleurs
│   │   └── constants.py             # Nom de la base SQLite
│   ├── models/
│   │   ├── card.py                  # CardModel
│   │   ├── column.py                # ColumnModel
│   │   ├── notification.py          # NotificationModel
│   │   └── app_state.py             # AppState (état global)
│   ├── database/
│   │   ├── init_db.py               # Schéma SQLite + données par défaut
│   │   ├── columns_repo.py          # CRUD + reorder des colonnes
│   │   ├── cards_repo.py            # CRUD des cartes
│   │   ├── activities_repo.py       # Journal d'activité
│   │   └── notifications_repo.py    # CRUD des notifications
│   └── ui/
│       ├── responsive.py            # Breakpoints + routing
│       ├── chrome/
│       │   └── title_bar.py         # Barre de titre desktop
│       ├── sidebar/
│       │   └── sidebar.py           # Sidebar (desktop/tablet/drawer)
│       ├── kanban/
│       │   ├── board_view.py        # Vue Kanban desktop
│       │   ├── kanban_column.py     # Colonne desktop
│       │   └── task_card.py         # Carte de tâche
│       ├── mobile/
│       │   ├── mobile_kanban.py     # Kanban mobile (TabBar)
│       │   ├── mobile_list.py       # Liste mobile
│       │   ├── mobile_analytics.py  # Analytique mobile
│       │   └── mobile_title_bar.py  # Barre de titre mobile
│       ├── views/
│       │   ├── list_view.py         # Vue liste desktop
│       │   └── analytics_view.py    # Vue analytique desktop
│       ├── components/
│       │   ├── buttons.py           # PrimaryButton, GhostButton, NeonButton
│       │   ├── badges.py            # PriorityBadge, TagChip, DueDateBadge
│       │   ├── cards.py             # GlassCard, AnimatedCounter
│       │   └── progress.py          # ProgressBarCustom
│       └── dialogs/
│           ├── card_add.py          # Dialogue création de carte
│           ├── card_edit.py         # Dialogue édition de carte
│           ├── column_add.py        # Dialogue création de colonne
│           ├── column_edit.py       # Dialogue renommage de colonne
│           └── priority_selector.py # Sélecteur de priorité
└── tests/                           # Tests (réservé)
```

---

## Modèle de données

### CardModel

| Champ | Type | Description |
|-------|------|-------------|
| `id` | `int` | Clé primaire |
| `title` | `str` | Titre |
| `description` | `str` | Description longue |
| `color` | `str` | Couleur d'étiquette (hex ou `"transparent"`) |
| `priority` | `int` | 1=Basse, 2=Moyenne, 3=Haute, 4=Critique |
| `tags` | `str` | JSON array de strings |
| `due_date` | `str \| None` | Format `AAAA-MM-JJ` |
| `assignee` | `str \| None` | Nom de l'assigné |
| `checklist` | `str` | JSON array (réservé) |
| `attachments` | `int` | Nombre de pièces jointes |
| `comments_count` | `int` | Nombre de commentaires |
| `column_id` | `int` | Clé étrangère vers `columns` |
| `created_at` | `str` | Horodatage création |
| `updated_at` | `str` | Horodatage dernière modification |

### ColumnModel

| Champ | Type | Description |
|-------|------|-------------|
| `id` | `int` | Clé primaire |
| `title` | `str` | Titre affiché |
| `color` | `str` | Couleur de la barre verticale (hex) |
| `position` | `int` | Ordre d'affichage (0 = première) |
| `created_at` | `str` | Horodatage création |

### NotificationModel

| Champ | Type | Description |
|-------|------|-------------|
| `id` | `int` | Clé primaire |
| `type` | `str` | `card_created`, `card_moved`, `card_updated`, `card_deleted`, `card_overdue`, `column_created`, `column_deleted` |
| `priority` | `str` | `info`, `success`, `warning` |
| `title` | `str` | Titre court |
| `message` | `str` | Description détaillée |
| `icon` | `str` | Clé d'icône (`info`, `warning`, `success`) |
| `read` | `bool` | `True` si lue |
| `created_at` | `str` | Horodatage |

### AppState

État global de l'application, transporté entre les composants :

```python
@dataclass
class AppState:
    columns: List[ColumnModel]
    all_cards: List[CardModel]
    notifications: List[NotificationModel]
    search_query: str
    filter_priority: Optional[int]
    filter_color: Optional[str]
    sidebar_open: bool
    notifications_open: bool
    view_mode: str  # "board" | "list" | "analytics"
    is_mobile: bool
    page_width: float
```

---

## Système de notifications

### Types de notifications

| Type | Priorité | Déclencheur |
|------|----------|-------------|
| `card_created` | `success` | Création d'une carte |
| `card_moved` | `info` | Déplacement entre colonnes |
| `card_updated` | `info` | Modification des détails |
| `card_deleted` | `warning` | Suppression d'une carte |
| `card_overdue` | `warning` | Carte en retard détectée au démarrage |
| `column_created` | `success` | Création d'une colonne |
| `column_deleted` | `warning` | Suppression d'une colonne |

### API

```python
from src.database import add_notification, get_all_notifications, mark_all_read, clear_all_notifications

# Ajouter une notification
await add_notification(
    type_='card_created',
    title='Nouvelle carte : Tâche X',
    message='Ajoutée à la colonne « Backlog ».',
    priority='success',
    icon='success',
)

# Lire toutes les notifications
notifs = await get_all_notifications()

# Marquer toutes comme lues
await mark_all_read()

# Vider la table
await clear_all_notifications()
```

Les notifications sont automatiquement purgées au-delà de 50 entrées (les plus anciennes sont supprimées).

---

## Persistance

La base SQLite `rivald_task.db` est créée à la racine du projet. Le schéma est défini dans `src/database/init_db.py`.

### Tables

- `columns` : colonnes Kanban.
- `cards` : cartes, liées à une colonne par clé étrangère.
- `activities` : journal d'activité (carte créée, modifiée, etc.).
- `notifications` : notifications utilisateur.

Toutes les opérations sont asynchrones via `aiosqlite`. Aucun ORM n'est utilisé : les requêtes sont écrites à la main pour rester explicites.

### Migration

Aucun système de migration n'est implémenté. Pour recréer la base :

```bash
rm rivald_task.db
python main.py  # La base est recréée avec les données par défaut
```

---

## Personnalisation

### Couleurs et espacements

Tous les tokens de design sont centralisés dans `src/config/theme.py` :

| Classe | Rôle |
|--------|------|
| `Spacing` | Grille de 8 px (8, 16, 24, 32, 48) |
| `Radius` | Rayons de bordure (6, 10, 14, 18) |
| `Duration` | Durées d'animation en ms (150, 200, 250) |
| `Easing` | Courbes d'animation Flet |
| `Layout` | Largeurs de colonnes, sidebar, header |
| `Typography` | Tailles de police (12 à 40 px) |
| `Theme` | Palette de couleurs, ombres, bordures |

Modifier une constante propage le changement à toute l'application au prochain lancement.

### Hauteur des colonnes Kanban

Dans `src/ui/kanban/kanban_column.py` (lignes 14–26) :

```python
MIN_COLUMN_HEIGHT = 420       # Hauteur minimum (px)
CARD_HEIGHT_ESTIMATE = 130    # Hauteur estimée par carte (px)
HEADER_HEIGHT = 56
ADD_BTN_HEIGHT = 48
COLUMN_PADDING = 24
```

### Nombre de colonnes par ligne (desktop)

Dans `src/config/theme.py` :

```python
class Layout:
    COLUMNS_PER_ROW = 5  # Modifiez cette valeur
```

### Points de rupture responsive

Dans `src/ui/responsive.py` :

```python
MOBILE_BREAKPOINT = 700
TABLET_BREAKPOINT = 1200
```

### Police

La police Inter est bundled dans `assets/fonts/`. Pour la remplacer, déposez un nouveau fichier TTF dans le même dossier et mettez à jour le mapping `page.fonts` dans `main.py`.

---

## API de configuration

### `main.py`

```python
import os
import flet as ft
from src.app import RivaldTaskApp
from src.config import Theme

async def main(page: ft.Page):
    page.title = "RivaldTask Pro"
    page.theme_mode = ft.ThemeMode.DARK
    page.bgcolor = Theme.BG_GLOBAL
    page.padding = 0

    # Icône de fenêtre (desktop uniquement)
    if not page.web and page.platform in (ft.PagePlatform.WINDOWS, ft.PagePlatform.MACOS, ft.PagePlatform.LINUX):
        icon_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "assets", "icon.png")
        if os.path.isfile(icon_path):
            page.window.icon = icon_path
        page.window.title_bar_hidden = True
        page.window.frameless = True

    # Police
    page.fonts = {"Inter": "/assets/fonts/Inter-Regular.ttf"}
    page.theme = ft.Theme(font_family="Inter")

    app = RivaldTaskApp(page)
    page.add(app)
    await app.init_and_load()

if __name__ == "__main__":
    ft.run(main, assets_dir="assets")
```

---

## Déploiement mobile

### Android

```bash
# Installer flet-cli
pip install flet-cli

# Lancer en mode développement (nécessite un téléphone sur le même réseau)
flet run --android main.py
```

### Build APK

```bash
flet build apk
```

L'APK est généré dans `build/apk/`.

### iOS

```bash
flet run --ios main.py
```

> **Note** : le build iOS nécessite macOS avec Xcode.

---

## Dépannage

### `NameError: name 'panel' is not defined`

Ce bug est corrigé dans la version actuelle. Si vous le rencontrez dans une version modifiée, vérifiez que `_build_notifications_panel()` assigne bien l'`AlertDialog` à une variable locale avant de le retourner, et que les closures `close_panel`/`clear_all` utilisent un `panel_holder = []` pour capturer la référence.

### `DragTargetEvent.__init__() missing 2 required positional arguments`

Ce crash se produisait sur Android avec Flet 0.85.3. Le client Android envoie des events drag sans `local_position`/`global_position`. **Correctif appliqué** : le drag & drop est désactivé sur mobile (`enable_drag=False`), les `TaskCard` et `KanbanColumn` n'étendent plus `ft.Draggable`/`ft.DragTarget` mais `ft.Container`. Le wrapping drag est appliqué externement dans `board_view.py`, uniquement sur desktop.

### L'icône de l'application ne s'affiche pas (Linux)

`page.window.icon` attend un **chemin de fichier absolu** sur disque, pas une URL d'asset Flet. Le code dans `main.py` calcule le chemin absolu via `os.path.dirname(os.path.abspath(__file__))`.

Si l'icône ne s'affiche toujours pas, vérifiez :

1. Que `assets/icon.png` existe (256x256 RGBA).
2. Que le chemin calculé est correct (`python -c "import os; print(os.path.join(os.path.dirname(os.path.abspath('main.py')), 'assets', 'icon.png'))"`).
3. Que votre gestionnaire de fenêtres supporte les icônes de fenêtre (la plupart le font).

### `DeprecationWarning: app() is deprecated`

Utilisez `ft.run(main, assets_dir="assets")` au lieu de `ft.app(main, assets_dir="assets")`. C'est déjà le cas dans le `main.py` actuel.

### La recherche perd le focus à chaque frappe

Ce bug est corrigé. `on_search_query_change()` ne reconstruit plus la sidebar, seul le `BoardView` est rafraîchi. La sidebar est conservée via `_sidebar_ref`.

### GTK warnings sur Linux

```
(flet:XXXXX): Gtk-WARNING **: Theme directory ... has no size field
```

Ces warnings proviennent du thème d'icônes système (ex: thème « Vintage »). Ils sont inoffensifs et n'affectent pas l'application. Pour les silencer, changez de thème d'icônes dans les paramètres système.

---

## Limites connues

- Les animations de transformation (scale, rotate) ne sont pas utilisées car Flet 0.85.3 ne les anime pas de manière fiable sur toutes les plateformes.
- Le drag & drop des colonnes ne fonctionne que sur desktop. Sur mobile, l'ordre des colonnes est fixe (utilisez le drag sur desktop pour réorganiser, puis la modification est synchronisée sur mobile au prochain chargement).
- Le badge PRO dans la barre de titre est purement décoratif. Aucune logique de licence n'est implémentée.
- L'avatar « U » en haut à droite est un placeholder. Aucune gestion de profil utilisateur n'est implémentée.
- Les notifications de cartes en retard sont générées une seule fois au démarrage. Elles ne sont pas ré-évaluées pendant la session.
- La vue tablette réutilise les composants desktop avec une sidebar rétrécie. Aucune vue tablette dédiée n'est implémentée.

---

## Licence

Projet privé. Tous droits réservés.
