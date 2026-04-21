import logging
import os
from PyQt6.QtWidgets import QMainWindow, QVBoxLayout, QWidget
from PyQt6.QtCore import QUrl

logger = logging.getLogger(__name__)
try:
    from PyQt6.QtWebEngineWidgets import QWebEngineView
    from PyQt6.QtWebChannel import QWebChannel
    WEBENGINE_AVAILABLE = True
except ImportError:
    WEBENGINE_AVAILABLE = False

from bridge import TaskyBridge

class MainWindow(QMainWindow):
    """Main Window hosting the React UI via QWebEngineView."""

    def __init__(self, db_manager=None):
        super().__init__()
        if db_manager is None:
            from database import DatabaseManager
            self.db_manager = DatabaseManager()
        else:
            self.db_manager = db_manager

        self.setWindowTitle("TASKY - Premium Task Manager")
        self.setMinimumSize(1200, 800)
        
        if not WEBENGINE_AVAILABLE:
            from PyQt6.QtWidgets import QLabel
            self.setCentralWidget(QLabel("Error: PyQt6-WebEngine not installed.\nPlease run: pip install PyQt6-WebEngine"))
            return

        self._setup_ui()

    def _setup_ui(self):
        central = QWidget()
        self.setCentralWidget(central)
        layout = QVBoxLayout(central)
        layout.setContentsMargins(0, 0, 0, 0)

        # Web View
        self.web_view = QWebEngineView()
        from PyQt6.QtGui import QColor
        self.web_view.page().setBackgroundColor(QColor("#030213")) # Matches your dark theme background
        layout.addWidget(self.web_view)

        # Bridge
        self.bridge = TaskyBridge(self.db_manager)
        self.channel = QWebChannel()
        self.channel.registerObject("pybridge", self.bridge)
        self.web_view.page().setWebChannel(self.channel)

        # Load UI
        # Priority: 1. Dev Server (localhost:5173/5174) 2. Built Files (web/dist/index.html)
        dist_path = os.path.normpath(os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "web", "dist", "index.html"))
        
        loaded = False
        # Try dev servers first if we're in a dev environment
        for port in [5173, 5174]:
            dev_url = f"http://localhost:{port}"
            try:
                import urllib.request
                # Short timeout to avoid blocking startup
                with urllib.request.urlopen(dev_url, timeout=0.5) as response:
                    if response.status == 200:
                        self.web_view.setUrl(QUrl(dev_url))
                        logger.debug("Loading from dev server: %s", dev_url)
                        loaded = True
                        break
            except Exception:
                continue

        if not loaded:
            if os.path.exists(dist_path):
                logger.debug("Loading from local file: %s", dist_path)
                self.web_view.setUrl(QUrl.fromLocalFile(dist_path))
            else:
                # Fallback to 5173 if nothing else found
                self.web_view.setUrl(QUrl("http://localhost:5173"))

        # Optional: Debugging
        # self.web_view.page().setDevToolsPage(self.web_view.page()) # Not quite right, but can be enabled

    def _open_pomodoro(self):
        # This is called from TrayManager
        # We can notify the JS side or just show the window
        self.show()
        self.raise_()
        self.activateWindow()
        # To switch tab in JS, we'd need to emit a signal via bridge or execute JS
        self.web_view.page().runJavaScript("window.location.hash = '#/timer'") # Example if using hash routing

    def load_tasks(self):
        """Triggers a data refresh in the React UI."""
        self.bridge.dataChanged.emit()

