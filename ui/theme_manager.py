import dataclasses
from PyQt6.QtCore import QObject, pyqtSignal, QSettings
from PyQt6.QtGui import QPalette, QColor, QFontDatabase
from PyQt6.QtWidgets import QApplication


@dataclasses.dataclass(frozen=True)
class DesignTokens:
    # Spacing
    space_1: int = 4
    space_2: int = 8
    space_3: int = 12
    space_4: int = 16
    space_5: int = 20
    space_6: int = 24

    # Border radius
    radius_sm: int = 8
    radius_md: int = 12
    radius_lg: int = 16
    radius_xl: int = 24
    radius_full: int = 999

    # Sizes
    accent_strip_width: int = 6
    card_border_width: int = 1
    header_height: int = 56
    sidebar_width: int = 240
    sidebar_collapsed: int = 48

    # Font sizes
    font_xs: int = 10
    font_sm: int = 11
    font_base: int = 13
    font_lg: int = 15
    font_xl: int = 18
    font_2xl: int = 24


TOKENS = DesignTokens()


class ThemeManager(QObject):
    """Manages application themes (dark/light) with QSettings persistence."""
    _instance = None

    @classmethod
    def instance(cls):
        return cls._instance

    theme_changed = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        ThemeManager._instance = self
        self._settings = QSettings("TASKY", "TASKY")
        self.current_theme = self._settings.value("theme", "dark")
        self._setup_themes()

    def _setup_themes(self):
        self.themes = {
            "dark": {
                "name": "Dark",
                "colors": {
                    "primary": "#fafafa",
                    "primary_hover": "#ffffff",
                    "primary_gradient_start": "#fafafa",
                    "primary_gradient_end": "#ffffff",
                    "secondary": "#27272a",
                    "secondary_hover": "#3f3f46",
                    "success": "#10B981",
                    "success_hover": "#059669",
                    "success_subtle": "rgba(16, 185, 129, 0.12)",
                    "success_text": "#34D399",
                    "warning": "#F59E0B",
                    "warning_hover": "#D97706",
                    "danger": "#EF4444",
                    "danger_hover": "#DC2626",
                    "info": "#3B82F6",
                    "info_hover": "#2563EB",

                    # Flat neutral surfaces
                    "surface_0": "#09090b",
                    "surface_1": "#0c0c0e",
                    "surface_2": "#18181b",
                    "surface_3": "#27272a",
                    "surface_4": "#3f3f46",
                    "surface_hover": "rgba(255, 255, 255, 0.05)",

                    # Aliases
                    "background": "#09090b",
                    "surface": "#09090b",
                    "surface_2_compat": "#18181b",
                    "border": "rgba(255, 255, 255, 0.08)",
                    "border_light": "rgba(255, 255, 255, 0.12)",
                    "border_subtle": "rgba(255, 255, 255, 0.04)",
                    "border_glow": "rgba(255, 255, 255, 0.15)",

                    # Text
                    "text_primary": "#fafafa",
                    "text_secondary": "#a1a1aa",
                    "text_muted": "#71717a",
                    "accent": "#8b5cf6",
                    "accent_hover": "#a78bfa",

                    # Priority
                    "priority_high": "#ef4444",
                    "priority_medium": "#71717a",
                    "priority_low": "#27272a",
                    "priority_none": "#18181b",

                    # Sidebar
                    "sidebar_bg": "#09090b",
                    "sidebar_item": "#09090b",
                    "sidebar_item_hover": "rgba(255, 255, 255, 0.05)",
                    "sidebar_active": "#27272a",
                    "sidebar_active_start": "#27272a",
                    "sidebar_active_end": "#27272a",
                    "sidebar_active_border": "#fafafa",

                    # Cards
                    "card_bg": "#09090b",
                    "card_hover": "#18181b",
                    "card_border": "rgba(255, 255, 255, 0.06)",
                    "card_completed_bg": "#09090b",
                    "card_completed_border": "rgba(255, 255, 255, 0.04)",
                    "card_overdue_bg": "#09090b",
                    "card_overdue_border": "#7F1D1D",

                    # Status chips
                    "chip_overdue_bg": "rgba(239, 68, 68, 0.12)",
                    "chip_overdue_text": "#fca5a5",
                    "chip_today_bg": "rgba(245, 158, 11, 0.12)",
                    "chip_today_text": "#fcd34d",
                    "chip_soon_bg": "rgba(59, 130, 246, 0.12)",
                    "chip_soon_text": "#93c5fd",
                    "chip_future_bg": "#18181b",
                    "chip_future_text": "#a1a1aa",
                    "chip_completed_bg": "rgba(16, 185, 129, 0.12)",
                    "chip_completed_text": "#6ee7b7",

                    # Priority chips
                    "chip_high_bg": "rgba(239, 68, 68, 0.12)",
                    "chip_high_text": "#fca5a5",
                    "chip_medium_bg": "#18181b",
                    "chip_medium_text": "#a1a1aa",
                    "chip_low_bg": "#18181b",
                    "chip_low_text": "#71717a",

                    # Scrollbar
                    "scrollbar_thumb": "#27272a",
                    "scrollbar_thumb_hover": "#3f3f46",

                    # Header
                    "header_bg": "#09090b",
                    "header_border": "rgba(255, 255, 255, 0.08)",
                },
            },
            "grey": {
                "name": "Slate Gray",
                "colors": {
                    # ── Core brand ─────────────────────────────────────────
                    "primary": "#6D8196",           # slate gray (base)
                    "primary_hover": "#ADCCED",     # light steel blue hover
                    "primary_gradient_start": "#546373",
                    "primary_gradient_end": "#6D8196",
                    "secondary": "#546373",
                    "secondary_hover": "#6D8196",

                    # ── Semantic ────────────────────────────────────────────
                    "success": "#4CA98A",
                    "success_hover": "#3A8A70",
                    "success_subtle": "rgba(76, 169, 138, 0.12)",
                    "success_text": "#7DCBB0",
                    "warning": "#B89460",
                    "warning_hover": "#9A7A4A",
                    "danger": "#C96070",
                    "danger_hover": "#A84858",
                    "info": "#5B8DB8",
                    "info_hover": "#4272A0",

                    # ── Elevation surfaces (darkest → lightest) ────────────
                    "surface_0": "#22292F",         # near-black slate
                    "surface_1": "#2C343C",         # based on #36404A lightened
                    "surface_2": "#36404A",         # #36404A exactly
                    "surface_3": "#546373",         # #546373
                    "surface_4": "#6D8196",         # #6D8196
                    "surface_hover": "#3E4C58",

                    # ── Aliases for compatibility ──────────────────────────
                    "background": "#22292F",
                    "surface": "#2C343C",
                    "surface_2_compat": "#36404A",
                    "border": "rgba(173, 204, 237, 0.12)",
                    "border_light": "rgba(173, 204, 237, 0.22)",
                    "border_subtle": "rgba(173, 204, 237, 0.05)",
                    "border_glow": "rgba(109, 129, 150, 0.35)",

                    # ── Text ────────────────────────────────────────────────
                    "text_primary": "#DDE6EF",      # cool off-white
                    "text_secondary": "#ADCCED",    # light steel blue
                    "text_muted": "#6D8196",        # muted slate
                    "accent": "#ADCCED",            # light steel blue accent
                    "accent_hover": "#C8DDEF",

                    # ── Priority ────────────────────────────────────────────
                    "priority_high": "#C96070",
                    "priority_medium": "#6D8196",
                    "priority_low": "#546373",
                    "priority_none": "#36404A",

                    # ── Sidebar ─────────────────────────────────────────────
                    "sidebar_bg": "#22292F",
                    "sidebar_item": "#22292F",
                    "sidebar_active": "rgba(109, 129, 150, 0.18)",
                    "sidebar_active_start": "rgba(109, 129, 150, 0.18)",
                    "sidebar_active_end": "#22292F",
                    "sidebar_active_border": "#ADCCED",

                    # ── Cards ────────────────────────────────────────────────
                    "card_bg": "#2C343C",
                    "card_hover": "#36404A",
                    "card_border": "rgba(173, 204, 237, 0.1)",
                    "card_completed_bg": "#252D34",
                    "card_completed_border": "rgba(173, 204, 237, 0.05)",
                    "card_overdue_bg": "#2E2527",
                    "card_overdue_border": "#7A4048",

                    # ── Status chips ─────────────────────────────────────────
                    "chip_overdue_bg": "rgba(201, 96, 112, 0.15)",
                    "chip_overdue_text": "#E08090",
                    "chip_today_bg": "rgba(184, 148, 96, 0.15)",
                    "chip_today_text": "#D4AF78",
                    "chip_soon_bg": "rgba(91, 141, 184, 0.15)",
                    "chip_soon_text": "#ADCCED",
                    "chip_future_bg": "#36404A",
                    "chip_future_text": "#ADCCED",
                    "chip_completed_bg": "rgba(76, 169, 138, 0.15)",
                    "chip_completed_text": "#7DCBB0",

                    # ── Priority chips ────────────────────────────────────────
                    "chip_high_bg": "rgba(201, 96, 112, 0.18)",
                    "chip_high_text": "#E8A0A8",
                    "chip_medium_bg": "rgba(109, 129, 150, 0.18)",
                    "chip_medium_text": "#ADCCED",
                    "chip_low_bg": "#36404A",
                    "chip_low_text": "#6D8196",

                    # ── Scrollbar ─────────────────────────────────────────────
                    "scrollbar_thumb": "rgba(109, 129, 150, 0.25)",
                    "scrollbar_thumb_hover": "rgba(173, 204, 237, 0.4)",

                    # ── Header ────────────────────────────────────────────────
                    "header_bg": "#22292F",
                    "header_border": "rgba(173, 204, 237, 0.1)",
                },
            },
            "light": {
                "name": "Light Mode",
                "colors": {
                    "primary": "#4F46E5",
                    "primary_hover": "#4338CA",
                    "primary_gradient_start": "#6366F1",
                    "primary_gradient_end": "#4F46E5",
                    "secondary": "#94A3B8",
                    "secondary_hover": "#64748B",
                    "success": "#0D9488",
                    "success_hover": "#0F766E",
                    "success_subtle": "#CCFBF1",
                    "success_text": "#115E59",
                    "warning": "#B45309",
                    "warning_hover": "#92400E",
                    "danger": "#E11D48",
                    "danger_hover": "#BE123C",
                    "info": "#2563EB",
                    "info_hover": "#1D4ED8",

                    # Elevation surfaces
                    "surface_0": "#F1F5F9",
                    "surface_1": "#F8FAFC",
                    "surface_2": "#FFFFFF",
                    "surface_3": "#F1F5F9",
                    "surface_4": "#E2E8F0",
                    "surface_hover": "#F8FAFC",

                    # Aliases for compatibility
                    "background": "#F8FAFC",
                    "surface": "#FFFFFF",
                    "surface_2_compat": "#F1F5F9",
                    "border": "rgba(100, 116, 139, 0.15)",
                    "border_light": "rgba(100, 116, 139, 0.25)",
                    "border_subtle": "rgba(0, 0, 0, 0.03)",
                    "border_glow": "rgba(79, 70, 229, 0.15)",

                    # Text
                    "text_primary": "#0F172A",
                    "text_secondary": "#475569",
                    "text_muted": "#94A3B8",
                    "accent": "#4F46E5",
                    "accent_hover": "#312E81",

                    # Priority
                    "priority_high": "#7E22CE",
                    "priority_medium": "#4F46E5",
                    "priority_low": "#64748B",
                    "priority_none": "#94A3B8",

                    # Sidebar
                    "sidebar_bg": "#F1F5F9",
                    "sidebar_item": "#F8FAFC",
                    "sidebar_active": "#EEF2FF",
                    "sidebar_active_start": "#EEF2FF",
                    "sidebar_active_end": "#E0E7FF",
                    "sidebar_active_border": "#6366F1",

                    # Cards
                    "card_bg": "#FFFFFF",
                    "card_hover": "#F8FAFC",
                    "card_border": "rgba(100, 116, 139, 0.2)",
                    "card_completed_bg": "#F8FAFC",
                    "card_completed_border": "rgba(100, 116, 139, 0.1)",
                    "card_overdue_bg": "#FFF1F2",
                    "card_overdue_border": "#FECDD3",

                    # Status chips
                    "chip_overdue_bg": "#FFE4E6",
                    "chip_overdue_text": "#BE123C",
                    "chip_today_bg": "#FEF3C7",
                    "chip_today_text": "#92400E",
                    "chip_soon_bg": "#DBEAFE",
                    "chip_soon_text": "#1D4ED8",
                    "chip_future_bg": "#F1F5F9",
                    "chip_future_text": "#475569",
                    "chip_completed_bg": "#CCFBF1",
                    "chip_completed_text": "#0F766E",

                    # Priority chips
                    "chip_high_bg": "#F3E8FF",
                    "chip_high_text": "#7E22CE",
                    "chip_medium_bg": "#E0E7FF",
                    "chip_medium_text": "#4338CA",
                    "chip_low_bg": "#F1F5F9",
                    "chip_low_text": "#475569",

                    # Scrollbar
                    "scrollbar_thumb": "rgba(100, 116, 139, 0.2)",
                    "scrollbar_thumb_hover": "rgba(100, 116, 139, 0.4)",

                    # Header
                    "header_bg": "#FFFFFF",
                    "header_border": "rgba(100, 116, 139, 0.15)",
                },
            },
        }

    def get_color(self, color_name: str) -> str:
        return self.themes[self.current_theme]["colors"].get(color_name, "#000000")

    def get_theme_colors(self) -> dict:
        return self.themes[self.current_theme]["colors"]

    def get_theme_name(self) -> str:
        return self.themes[self.current_theme]["name"]

    def is_dark(self) -> bool:
        return self.current_theme in ["dark", "grey"]

    def get_theme_icon(self) -> str:
        if self.current_theme == "dark": return "◑"
        if self.current_theme == "grey": return "◈"   # slate gray indicator
        return "◐"

    def set_theme(self, theme_name: str):
        if theme_name in self.themes:
            self.current_theme = theme_name
            self._settings.setValue("theme", theme_name)
            self.theme_changed.emit(theme_name)

    def toggle_theme(self):
        order = ["dark", "light", "grey"]
        idx = order.index(self.current_theme) if self.current_theme in order else 0
        self.set_theme(order[(idx + 1) % len(order)])

    def get_font_family(self) -> str:
        families = QFontDatabase.families()
        for candidate in ["Inter", "SF Pro Display", "SF Pro Text", "Segoe UI", "Helvetica Neue"]:
            if any(candidate.lower() in f.lower() for f in families):
                return candidate
        return "Arial"

    @staticmethod
    def load_inter_font(font_dir: str) -> bool:
        import os
        loaded = False
        for fname in ["Inter-Regular.ttf", "Inter-Medium.ttf", "Inter-SemiBold.ttf", "Inter-Bold.ttf"]:
            path = os.path.join(font_dir, fname)
            if os.path.exists(path):
                QFontDatabase.addApplicationFont(path)
                loaded = True
        return loaded

    def apply_theme_to_app(self, app: QApplication):
        colors = self.get_theme_colors()
        palette = QPalette()
        bg = QColor(colors["background"])
        surface = QColor(colors["surface"])
        text = QColor(colors["text_primary"])
        primary = QColor(colors["primary"])
        danger = QColor(colors["danger"])

        palette.setColor(QPalette.ColorRole.Window, bg)
        palette.setColor(QPalette.ColorRole.WindowText, text)
        palette.setColor(QPalette.ColorRole.Base, surface)
        palette.setColor(QPalette.ColorRole.AlternateBase, QColor(colors["surface_2"]))
        palette.setColor(QPalette.ColorRole.ToolTipBase, surface)
        palette.setColor(QPalette.ColorRole.ToolTipText, text)
        palette.setColor(QPalette.ColorRole.Text, text)
        palette.setColor(QPalette.ColorRole.Button, surface)
        palette.setColor(QPalette.ColorRole.ButtonText, text)
        palette.setColor(QPalette.ColorRole.BrightText, danger)
        palette.setColor(QPalette.ColorRole.Link, primary)
        palette.setColor(QPalette.ColorRole.Highlight, primary)
        palette.setColor(QPalette.ColorRole.HighlightedText, QColor("#ffffff"))
        palette.setColor(QPalette.ColorRole.PlaceholderText, QColor(colors["text_muted"]))
        app.setPalette(palette)

    # ── Stylesheet helpers (one method per widget group) ──────────────────────

    def _base_style(self, c: dict, font: str) -> str:
        return f"""
        QMainWindow, QDialog {{
            background-color: {c['background']};
            color: {c['text_primary']};
            font-family: '{font}', 'Segoe UI', sans-serif;
        }}
        QWidget {{
            background-color: {c['background']};
            color: {c['text_primary']};
            font-family: '{font}', 'Segoe UI', sans-serif;
            font-size: 13px;
        }}
        QLabel {{
            background-color: transparent;
            color: {c['text_primary']};
        }}
        """

    def _button_style(self, c: dict, ghost_hover: str, ghost_checked: str) -> str:
        return f"""
        QPushButton {{
            background: {c['primary']};
            color: #ffffff;
            border: none;
            border-radius: {TOKENS.radius_sm}px;
            padding: 8px 20px;
            font-weight: 600;
            font-size: 13px;
            min-height: 36px;
        }}
        QPushButton:hover {{ background: {c['primary_hover']}; }}
        QPushButton:pressed {{ background: {c['primary_gradient_start']}; }}
        QPushButton:disabled {{ background: {c['surface_3']}; color: {c['text_muted']}; }}
        QPushButton[class="success"] {{ background: {c['success_subtle']}; color: {c['success_text']}; }}
        QPushButton[class="success"]:hover {{ background: {c['success']}; color: #ffffff; }}
        QPushButton[class="warning"] {{ background: {c['chip_today_bg']}; color: {c['chip_today_text']}; }}
        QPushButton[class="warning"]:hover {{ background: {c['warning']}; color: #ffffff; }}
        QPushButton[class="danger"] {{ background: {c['chip_overdue_bg']}; color: {c['chip_overdue_text']}; }}
        QPushButton[class="danger"]:hover {{ background: {c['danger']}; color: #ffffff; }}
        QPushButton[class="info"] {{ background: {c['chip_soon_bg']}; color: {c['chip_soon_text']}; }}
        QPushButton[class="secondary"] {{
            background: {c['surface_2']};
            color: {c['text_primary']};
            border: 1px solid {c['border']};
        }}
        QPushButton[class="secondary"]:hover {{ background: {c['surface_3']}; border-color: {c['primary']}; }}
        QPushButton[class="ghost"] {{ background: transparent; color: {c['text_secondary']}; border: none; }}
        QPushButton[class="ghost"]:hover {{ background: {ghost_hover}; color: {c['primary']}; }}
        QPushButton[class="ghost"]:checked {{ background: {ghost_checked}; color: {c['primary']}; }}
        """

    def _input_style(self, c: dict) -> str:
        return f"""
        QLineEdit, QTextEdit, QPlainTextEdit {{
            background-color: {c['surface_1']};
            color: {c['text_primary']};
            border: 1.5px solid {c['border']};
            border-radius: {TOKENS.radius_sm}px;
            padding: 9px 12px;
            font-size: 13px;
            selection-background-color: {c['primary']};
        }}
        QLineEdit:focus, QTextEdit:focus, QPlainTextEdit:focus {{
            border-color: {c['primary']};
            background-color: {c['surface_2']};
            outline: none;
        }}
        QLineEdit:hover, QTextEdit:hover {{ border-color: {c['border_light']}; }}
        QDateTimeEdit, QSpinBox, QComboBox {{
            background-color: {c['surface_1']};
            color: {c['text_primary']};
            border: 1.5px solid {c['border']};
            border-radius: {TOKENS.radius_sm}px;
            padding: 7px 10px;
            font-size: 13px;
            min-height: 36px;
        }}
        QDateTimeEdit:focus, QSpinBox:focus, QComboBox:focus {{
            border-color: {c['primary']};
            background-color: {c['surface_2']};
        }}
        QComboBox::drop-down {{ border: none; width: 30px; padding-right: 4px; }}
        QComboBox::down-arrow {{ image: none; border: none; width: 0px; }}
        QComboBox QAbstractItemView {{
            background-color: {c['surface_2']};
            color: {c['text_primary']};
            border: 1px solid {c['border']};
            border-radius: {TOKENS.radius_md}px;
            padding: 6px;
            selection-background-color: {c['primary']};
            outline: 0px;
        }}
        QComboBox QAbstractItemView::item {{ padding: 6px 12px; border-radius: 6px; min-height: 28px; }}
        QComboBox QAbstractItemView::item:selected {{ background: {c['primary']}; color: #ffffff; }}
        QSpinBox::up-button, QSpinBox::down-button {{
            background: {c['surface_4']}; border: none; border-radius: 4px; width: 18px;
        }}
        QSpinBox::up-button:hover, QSpinBox::down-button:hover {{ background: {c['primary']}; }}
        """

    def _checkbox_style(self, c: dict) -> str:
        return f"""
        QCheckBox {{ color: {c['text_primary']}; spacing: 10px; font-size: 13px; }}
        QCheckBox::indicator {{
            width: 20px; height: 20px;
            border: 2.5px solid {c['border']};
            border-radius: 6px;
            background-color: {c['surface_1']};
        }}
        QCheckBox::indicator:hover {{ border-color: {c['primary']}; }}
        QCheckBox::indicator:checked {{ background: {c['primary']}; border-color: {c['primary']}; }}
        """

    def _list_style(self, c: dict) -> str:
        return f"""
        QListWidget {{
            background-color: {c['surface_1']};
            color: {c['text_primary']};
            border: 1.5px solid {c['border']};
            border-radius: {TOKENS.radius_md}px;
            padding: 6px;
            outline: 0px;
        }}
        QListWidget::item {{ padding: 8px 12px; border-radius: 8px; margin: 1px 0px; min-height: 28px; }}
        QListWidget::item:selected {{ background: {c['sidebar_active']}; color: {c['primary']}; font-weight: 600; }}
        QListWidget::item:hover {{ background-color: {c['surface_2']}; }}
        """

    def _scrollbar_style(self, c: dict) -> str:
        return f"""
        QScrollBar:vertical {{ background-color: transparent; width: 10px; margin: 0; }}
        QScrollBar::handle:vertical {{
            background-color: {c['scrollbar_thumb']}; border-radius: 5px; min-height: 30px; margin: 2px;
        }}
        QScrollBar::handle:vertical:hover {{ background-color: {c['scrollbar_thumb_hover']}; }}
        QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {{ height: 0; }}
        QScrollBar:horizontal {{ background-color: transparent; height: 10px; margin: 0; }}
        QScrollBar::handle:horizontal {{
            background-color: {c['scrollbar_thumb']}; border-radius: 5px; min-width: 30px; margin: 2px;
        }}
        QScrollBar::handle:horizontal:hover {{ background-color: {c['scrollbar_thumb_hover']}; }}
        QScrollBar::add-line:horizontal, QScrollBar::sub-line:horizontal {{ width: 0; }}
        """

    def _menu_style(self, c: dict, menu_sel_bg: str, tab_hover_bg: str) -> str:
        return f"""
        QStatusBar {{
            background-color: {c['surface_2']}; color: {c['text_muted']};
            border-top: 1px solid {c['border']}; font-size: 11px;
        }}
        QMenuBar {{
            background-color: {c['surface_2']}; color: {c['text_primary']};
            border-bottom: 1px solid {c['border']}; padding: 2px;
        }}
        QMenuBar::item {{ background-color: transparent; padding: 5px 12px; border-radius: 6px; }}
        QMenuBar::item:selected {{ background: {menu_sel_bg}; color: {c['primary']}; }}
        QMenu {{
            background-color: {c['surface_2']}; color: {c['text_primary']};
            border: 1px solid {c['border']}; border-radius: {TOKENS.radius_md}px; padding: 6px;
        }}
        QMenu::item {{ padding: 8px 28px 8px 12px; border-radius: 8px; margin: 1px 0px; font-size: 13px; min-height: 30px; }}
        QMenu::item:selected {{ background: {c['primary']}; color: #ffffff; }}
        QMenu::separator {{ height: 1px; background-color: {c['border']}; margin: 4px 8px; }}
        QTabWidget::pane {{
            border: 1px solid {c['border']}; border-radius: {TOKENS.radius_lg}px;
            background-color: {c['surface_1']}; top: -1px;
        }}
        QTabBar::tab {{
            background-color: transparent; color: {c['text_secondary']};
            padding: 10px 24px; border-radius: 20px; font-weight: 600;
            font-size: 12px; margin: 4px 4px; min-width: 80px;
        }}
        QTabBar::tab:selected {{ background: {c['primary']}; color: #ffffff; }}
        QTabBar::tab:hover:!selected {{ background: {tab_hover_bg}; color: {c['primary']}; }}
        """

    def _misc_style(self, c: dict) -> str:
        return f"""
        QToolTip {{
            background-color: {c['surface_4']}; color: {c['text_primary']};
            border: 1px solid {c['primary']}; border-radius: 6px; padding: 6px 10px; font-size: 11px;
        }}
        QSplitter::handle {{ background-color: {c['border']}; width: 1px; }}
        QFrame[frameShape="4"], QFrame[frameShape="5"] {{ color: {c['border']}; }}
        QSlider::groove:horizontal {{ background-color: {c['surface_3']}; height: 4px; border-radius: 2px; }}
        QSlider::handle:horizontal {{
            background: {c['primary']}; width: 16px; height: 16px; border-radius: 8px; margin: -6px 0;
        }}
        QSlider::sub-page:horizontal {{ background: {c['primary']}; border-radius: 2px; }}
        QProgressBar {{
            background-color: {c['surface_2']}; border: none; border-radius: 4px;
            text-align: center; font-size: 10px; color: transparent;
        }}
        QProgressBar::chunk {{
            background: qlineargradient(x1:0, y1:0, x2:1, y2:0,
                stop:0 {c['primary_gradient_start']}, stop:1 {c['primary_gradient_end']});
            border-radius: 4px;
        }}
        """

    def get_stylesheet(self) -> str:
        c = self.get_theme_colors()
        font = self.get_font_family()
        t = self.current_theme
        is_dark = self.is_dark()

        if t == "grey":
            ghost_hover   = "rgba(109, 129, 150, 0.14)"
            ghost_checked = "rgba(109, 129, 150, 0.22)"
            menu_sel_bg   = "rgba(84,  99, 115, 0.40)"
            tab_hover_bg  = "rgba(84,  99, 115, 0.32)"
        elif is_dark:
            ghost_hover   = "rgba(255, 255, 255, 0.06)"
            ghost_checked = "rgba(255, 255, 255, 0.10)"
            menu_sel_bg   = "rgba(255, 255, 255, 0.06)"
            tab_hover_bg  = "rgba(255, 255, 255, 0.05)"
        else:
            ghost_hover   = "rgba(79, 70, 229, 0.08)"
            ghost_checked = "rgba(79, 70, 229, 0.12)"
            menu_sel_bg   = "rgba(107, 114, 128, 0.11)"
            tab_hover_bg  = "rgba(107, 114, 128, 0.08)"

        return "".join([
            self._base_style(c, font),
            self._button_style(c, ghost_hover, ghost_checked),
            self._input_style(c),
            self._checkbox_style(c),
            self._list_style(c),
            self._scrollbar_style(c),
            self._menu_style(c, menu_sel_bg, tab_hover_bg),
            self._misc_style(c),
        ])


class AnimationHelper:
    """Factory for reusable QPropertyAnimation patterns."""

    @staticmethod
    def fade_in(widget, duration: int = 200, start: float = 0.0, end: float = 1.0):
        from PyQt6.QtWidgets import QGraphicsOpacityEffect
        from PyQt6.QtCore import QPropertyAnimation, QEasingCurve
        effect = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(effect)
        effect.setOpacity(start)
        anim = QPropertyAnimation(effect, b"opacity", widget)
        anim.setDuration(duration)
        anim.setStartValue(start)
        anim.setEndValue(end)
        anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        anim.start()
        return anim

    @staticmethod
    def slide_in_from_bottom(widget, duration: int = 260):
        from PyQt6.QtCore import QPropertyAnimation, QPoint, QEasingCurve
        from PyQt6.QtWidgets import QGraphicsOpacityEffect
        widget.show()
        effect = QGraphicsOpacityEffect(widget)
        widget.setGraphicsEffect(effect)
        effect.setOpacity(0.0)
        op_anim = QPropertyAnimation(effect, b"opacity", widget)
        op_anim.setDuration(duration)
        op_anim.setStartValue(0.0)
        op_anim.setEndValue(1.0)
        op_anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        op_anim.start()
        return op_anim

    @staticmethod
    def scale_in_dialog(dialog, duration: int = 220):
        from PyQt6.QtCore import QPropertyAnimation, QEasingCurve
        from PyQt6.QtWidgets import QGraphicsOpacityEffect
        effect = QGraphicsOpacityEffect(dialog)
        dialog.setGraphicsEffect(effect)
        effect.setOpacity(0.0)
        anim = QPropertyAnimation(effect, b"opacity", dialog)
        anim.setDuration(duration)
        anim.setStartValue(0.0)
        anim.setEndValue(1.0)
        anim.setEasingCurve(QEasingCurve.Type.OutCubic)
        anim.start()
        return anim

    @staticmethod
    def color_flash(widget, from_color: str, to_color: str, duration: int = 400):
        from PyQt6.QtCore import QVariantAnimation, QEasingCurve
        from PyQt6.QtGui import QColor
        anim = QVariantAnimation(widget)
        anim.setDuration(duration)
        anim.setStartValue(QColor(from_color))
        anim.setEndValue(QColor(to_color))
        anim.setEasingCurve(QEasingCurve.Type.InOutSine)
        return anim
