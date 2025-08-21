from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtGui import QPalette, QColor
from PyQt6.QtWidgets import QApplication


class ThemeManager(QObject):
    """Manages application themes (dark and light mode)."""
    
    theme_changed = pyqtSignal(str)  # Signal emitted when theme changes
    
    def __init__(self):
        super().__init__()
        self.current_theme = "dark"
        self._setup_themes()
    
    def _setup_themes(self):
        """Set up the available themes."""
        self.themes = {
            "dark": {
                "name": "Dark Mode",
                "colors": {
                    "primary": "#8b5cf6",      # Purple
                    "primary_hover": "#7c3aed",
                    "secondary": "#3b82f6",    # Blue
                    "secondary_hover": "#2563eb",
                    "success": "#8b5cf6",      # Purple
                    "success_hover": "#7c3aed",
                    "warning": "#3b82f6",      # Blue
                    "warning_hover": "#2563eb",
                    "danger": "#ef4444",       # Red
                    "danger_hover": "#dc2626",
                    "info": "#3b82f6",         # Blue
                    "info_hover": "#2563eb",
                    "background": "#1f2937",   # Dark grey outer
                    "surface": "#374151",      # Grey inner
                    "surface_hover": "#4b5563", # Lighter grey hover
                    "border": "#4b5563",       # Grey border
                    "text_primary": "#f9fafb", # Light text
                    "text_secondary": "#d1d5db", # Medium text
                    "text_muted": "#9ca3af",   # Muted text
                    "accent": "#8b5cf6",       # Purple accent
                    "accent_hover": "#7c3aed",
                }
            },
            "light": {
                "name": "Light Mode",
                "colors": {
                    "primary": "#8b5cf6",      # Purple
                    "primary_hover": "#7c3aed",
                    "secondary": "#3b82f6",    # Blue
                    "secondary_hover": "#2563eb",
                    "success": "#8b5cf6",      # Purple
                    "success_hover": "#7c3aed",
                    "warning": "#3b82f6",      # Blue
                    "warning_hover": "#2563eb",
                    "danger": "#ef4444",       # Red
                    "danger_hover": "#dc2626",
                    "info": "#3b82f6",         # Blue
                    "info_hover": "#2563eb",
                    "background": "#e5e7eb",   # Dimmer light grey outer
                    "surface": "#f8fafc",      # Dimmed white inner
                    "surface_hover": "#f1f5f9", # Dimmer light grey hover
                    "border": "#cbd5e1",       # Dimmer grey border
                    "text_primary": "#1e293b", # Darker text for better contrast
                    "text_secondary": "#475569", # Medium text
                    "text_muted": "#64748b",   # Muted text
                    "accent": "#8b5cf6",       # Purple accent
                    "accent_hover": "#7c3aed",
                }
            }
        }
    
    def get_color(self, color_name: str) -> str:
        """Get a color from the current theme."""
        return self.themes[self.current_theme]["colors"].get(color_name, "#000000")
    
    def get_theme_colors(self) -> dict:
        """Get all colors for the current theme."""
        return self.themes[self.current_theme]["colors"]
    
    def get_theme_name(self) -> str:
        """Get the name of the current theme."""
        return self.themes[self.current_theme]["name"]
    
    def get_theme_icon(self) -> str:
        """Get the icon for the current theme toggle switch."""
        return "☀️🌙" if self.current_theme == "dark" else "🌙☀️"
    
    def set_theme(self, theme_name: str):
        """Set the current theme."""
        if theme_name in self.themes:
            self.current_theme = theme_name
            self.theme_changed.emit(theme_name)
    
    def toggle_theme(self):
        """Toggle between dark and light themes."""
        new_theme = "light" if self.current_theme == "dark" else "dark"
        self.set_theme(new_theme)
    
    def apply_theme_to_app(self, app: QApplication):
        """Apply the current theme to the QApplication."""
        colors = self.get_theme_colors()
        
        # Create palette
        palette = QPalette()
        
        if self.current_theme == "dark":
            # Dark theme palette
            palette.setColor(QPalette.ColorRole.Window, QColor(colors["background"]))
            palette.setColor(QPalette.ColorRole.WindowText, QColor(colors["text_primary"]))
            palette.setColor(QPalette.ColorRole.Base, QColor(colors["surface"]))
            palette.setColor(QPalette.ColorRole.AlternateBase, QColor(colors["surface_hover"]))
            palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(colors["surface"]))
            palette.setColor(QPalette.ColorRole.ToolTipText, QColor(colors["text_primary"]))
            palette.setColor(QPalette.ColorRole.Text, QColor(colors["text_primary"]))
            palette.setColor(QPalette.ColorRole.Button, QColor(colors["surface"]))
            palette.setColor(QPalette.ColorRole.ButtonText, QColor(colors["text_primary"]))
            palette.setColor(QPalette.ColorRole.BrightText, QColor(colors["danger"]))
            palette.setColor(QPalette.ColorRole.Link, QColor(colors["accent"]))
            palette.setColor(QPalette.ColorRole.Highlight, QColor(colors["primary"]))
            palette.setColor(QPalette.ColorRole.HighlightedText, QColor(colors["text_primary"]))
        else:
            # Light theme palette
            palette.setColor(QPalette.ColorRole.Window, QColor(colors["background"]))
            palette.setColor(QPalette.ColorRole.WindowText, QColor(colors["text_primary"]))
            palette.setColor(QPalette.ColorRole.Base, QColor(colors["surface"]))
            palette.setColor(QPalette.ColorRole.AlternateBase, QColor(colors["surface_hover"]))
            palette.setColor(QPalette.ColorRole.ToolTipBase, QColor(colors["surface"]))
            palette.setColor(QPalette.ColorRole.ToolTipText, QColor(colors["text_primary"]))
            palette.setColor(QPalette.ColorRole.Text, QColor(colors["text_primary"]))
            palette.setColor(QPalette.ColorRole.Button, QColor(colors["surface"]))
            palette.setColor(QPalette.ColorRole.ButtonText, QColor(colors["text_primary"]))
            palette.setColor(QPalette.ColorRole.BrightText, QColor(colors["danger"]))
            palette.setColor(QPalette.ColorRole.Link, QColor(colors["accent"]))
            palette.setColor(QPalette.ColorRole.Highlight, QColor(colors["primary"]))
            palette.setColor(QPalette.ColorRole.HighlightedText, QColor(colors["text_primary"]))
        
        app.setPalette(palette)
    
    def get_stylesheet(self) -> str:
        """Get the stylesheet for the current theme."""
        colors = self.get_theme_colors()
        
        return f"""
        /* Main Window */
        QMainWindow {{
            background-color: {colors['background']};
            color: {colors['text_primary']};
        }}
        
        /* Central Widget */
        QWidget {{
            background-color: {colors['background']};
            color: {colors['text_primary']};
        }}
        
        /* Labels */
        QLabel {{
            background-color: transparent;
            color: {colors['text_primary']};
        }}
        
        /* Buttons - Modern Attractive Design */
        QPushButton {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {colors['primary']}, stop:1 {colors['primary_hover']});
            color: white;
            border: none;
            border-radius: 8px;
            padding: 4px 8px;
            font-weight: 600;
            font-size: 10px;
            min-height: 24px;
            font-family: 'Segoe UI', sans-serif;
        }}
        
        QPushButton:hover {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {colors['primary_hover']}, stop:1 {colors['primary']});
        }}
        
        QPushButton:pressed {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {colors['primary_hover']}, stop:1 {colors['primary']});
        }}
        
        QPushButton:disabled {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {colors['surface_hover']}, stop:1 {colors['surface']});
            color: {colors['text_muted']};
        }}
        
        /* Small Buttons (for notification popup) */
        QPushButton[class="small"] {{
            min-height: 24px;
            padding: 4px 8px;
            font-size: 10px;
            border-radius: 6px;
        }}
        
        /* Success Button */
        QPushButton[class="success"] {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {colors['success']}, stop:1 {colors['success_hover']});
        }}
        
        QPushButton[class="success"]:hover {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {colors['success_hover']}, stop:1 {colors['success']});
        }}
        
        /* Warning Button */
        QPushButton[class="warning"] {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {colors['warning']}, stop:1 {colors['warning_hover']});
            color: {colors['text_primary']};
        }}
        
        QPushButton[class="warning"]:hover {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {colors['warning_hover']}, stop:1 {colors['warning']});
        }}
        
        /* Danger Button */
        QPushButton[class="danger"] {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {colors['danger']}, stop:1 {colors['danger_hover']});
        }}
        
        QPushButton[class="danger"]:hover {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {colors['danger_hover']}, stop:1 {colors['danger']});
        }}
        
        /* Info Button */
        QPushButton[class="info"] {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {colors['info']}, stop:1 {colors['info_hover']});
        }}
        
        QPushButton[class="info"]:hover {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {colors['info_hover']}, stop:1 {colors['info']});
        }}
        
        /* Secondary Button */
        QPushButton[class="secondary"] {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {colors['secondary']}, stop:1 {colors['secondary_hover']});
        }}
        
        QPushButton[class="secondary"]:hover {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {colors['secondary_hover']}, stop:1 {colors['secondary']});
        }}
        
        /* Theme Toggle Switch */
        QPushButton[class="secondary"] {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {colors['surface']}, stop:1 {colors['surface_hover']});
            border: 2px solid {colors['border']};
            border-radius: 15px;
            color: {colors['text_primary']};
            font-size: 12px;
            font-weight: bold;
            padding: 4px 8px;
        }}
        
        QPushButton[class="secondary"]:hover {{
            background: qlineargradient(x1:0, y1:0, x2:0, y2:1,
                stop:0 {colors['surface_hover']}, stop:1 {colors['border']});
            border-color: {colors['primary']};
        }}
        
        /* Table Widget */
        QTableWidget {{
            background-color: {colors['surface']};
            alternate-background-color: {colors['surface_hover']};
            gridline-color: {colors['border']};
            border: 1px solid {colors['border']};
            border-radius: 8px;
        }}
        
        QTableWidget::item {{
            padding: 8px;
            border: none;
        }}
        
        QTableWidget::item:selected {{
            background-color: {colors['primary']};
            color: white;
        }}
        
        QHeaderView::section {{
            background-color: {colors['surface_hover']};
            color: {colors['text_primary']};
            padding: 8px;
            border: none;
            font-weight: bold;
        }}
        
        /* Line Edit */
        QLineEdit {{
            background-color: {colors['surface']};
            color: {colors['text_primary']};
            border: 2px solid {colors['border']};
            border-radius: 6px;
            padding: 8px 12px;
            font-size: 13px;
        }}
        
        QLineEdit:focus {{
            border-color: {colors['primary']};
        }}
        
        /* Text Edit */
        QTextEdit {{
            background-color: {colors['surface']};
            color: {colors['text_primary']};
            border: 2px solid {colors['border']};
            border-radius: 6px;
            padding: 8px 12px;
            font-size: 13px;
        }}
        
        QTextEdit:focus {{
            border-color: {colors['primary']};
        }}
        
        /* DateTime Edit */
        QDateTimeEdit {{
            background-color: {colors['surface']};
            color: {colors['text_primary']};
            border: 2px solid {colors['border']};
            border-radius: 6px;
            padding: 8px 12px;
            font-size: 13px;
        }}
        
        QDateTimeEdit:focus {{
            border-color: {colors['primary']};
        }}
        
        /* Checkbox */
        QCheckBox {{
            color: {colors['text_primary']};
            spacing: 8px;
        }}
        
        QCheckBox::indicator {{
            width: 18px;
            height: 18px;
            border: 2px solid {colors['border']};
            border-radius: 4px;
            background-color: {colors['surface']};
        }}
        
        QCheckBox::indicator:checked {{
            background-color: {colors['primary']};
            border-color: {colors['primary']};
        }}
        
        /* Scroll Bar */
        QScrollBar:vertical {{
            background-color: {colors['surface']};
            width: 12px;
            border-radius: 6px;
        }}
        
        QScrollBar::handle:vertical {{
            background-color: {colors['border']};
            border-radius: 6px;
            min-height: 20px;
        }}
        
        QScrollBar::handle:vertical:hover {{
            background-color: {colors['text_muted']};
        }}
        
        /* Status Bar */
        QStatusBar {{
            background-color: {colors['surface']};
            color: {colors['text_secondary']};
            border-top: 1px solid {colors['border']};
        }}
        
        /* Menu Bar */
        QMenuBar {{
            background-color: {colors['surface']};
            color: {colors['text_primary']};
            border-bottom: 1px solid {colors['border']};
        }}
        
        QMenuBar::item {{
            background-color: transparent;
            padding: 8px 12px;
        }}
        
        QMenuBar::item:selected {{
            background-color: {colors['primary']};
            color: white;
        }}
        """
