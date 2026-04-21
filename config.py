"""Central application constants — import from here instead of scattering magic numbers."""

# ── Tray / UI ──────────────────────────────────────────────────────────────
TRAY_UPDATE_INTERVAL_MS = 60_000          # tooltip refresh period
NOTIFICATION_AUTO_CLOSE_MS = 25_000       # popup auto-dismiss
NOTIFICATION_PROGRESS_INTERVAL_MS = 1_000 # countdown tick

# ── Notifications ──────────────────────────────────────────────────────────
NOTIFICATION_RING_COUNT = 15              # max beep cycles before auto-stop
NOTIFICATION_RING_BEEP_HZ_LO = 880       # low beep frequency
NOTIFICATION_RING_BEEP_HZ_HI = 1100      # high beep frequency
NOTIFICATION_RING_BEEP_MS = 180          # beep duration
NOTIFICATION_RING_PAUSE_S = 1.8          # pause between beeps
NOTIFICATION_RING_FALLBACK_PAUSE_S = 2.0  # pause when no winsound
NOTIFICATION_STOP_AFTER_S = 10           # auto-stop ringing after this many seconds
NOTIFICATION_CHECK_INTERVAL_S = 60       # how often to poll for due tasks
NOTIFICATION_TOAST_MAX_CHARS = 80        # truncate message in OS toast

# ── Analytics ──────────────────────────────────────────────────────────────
ANALYTICS_DEFAULT_DAYS = 7

# ── App identity ───────────────────────────────────────────────────────────
APP_NAME = "TASKY"
APP_VERSION = "2.0.0"
APP_ORG = "TASKY"
