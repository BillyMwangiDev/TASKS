import { Outlet, Link, useLocation } from "react-router";
import { CheckSquare, Timer, BarChart3, Sun, Moon, Flame, Command, Settings } from "lucide-react";
import { useTaskyData } from "../hooks/useTaskyData";
import { useEffect, useState, useCallback } from "react";
import { CommandPalette } from "./CommandPalette";
import { DailyDigest } from "./DailyDigest";
import { SettingsModal } from "./SettingsModal";
import { useAI } from "../hooks/useAI";

export function Layout() {
  const location = useLocation();
  const { toggleTheme, theme, tasks, projects } = useTaskyData();
  const { getStreak, isAvailable } = useAI();

  const [paletteOpen, setPaletteOpen] = useState(false);
  const [captureOpen, setCaptureOpen] = useState(false);
  const [settingsOpen, setSettingsOpen] = useState(false);
  const [streak, setStreak] = useState(0);
  const [digestOpen, setDigestOpen] = useState(false);
  const [aiConfigured, setAiConfigured] = useState(true);

  // Load streak and AI status once on mount
  useEffect(() => {
    getStreak().then(setStreak);
    isAvailable().then(setAiConfigured);
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  // Refresh AI status when settings modal closes
  useEffect(() => {
    if (!settingsOpen) isAvailable().then(setAiConfigured);
  }, [settingsOpen]); // eslint-disable-line react-hooks/exhaustive-deps

  // Show daily digest once per day
  useEffect(() => {
    const key = `tasky_digest_${new Date().toISOString().slice(0, 10)}`;
    if (!localStorage.getItem(key)) {
      setTimeout(() => {
        setDigestOpen(true);
        localStorage.setItem(key, "1");
      }, 800);
    }
  }, []);

  const openNewTask = useCallback(() => {
    // Navigate to tasks then focus the input
    if (location.pathname !== "/") {
      window.location.href = "/";
    }
    setTimeout(() => {
      const el = document.getElementById("new-task-input");
      el?.focus();
    }, 100);
  }, [location.pathname]);

  // Global Ctrl+K shortcut
  useEffect(() => {
    const handler = (e: KeyboardEvent) => {
      if ((e.metaKey || e.ctrlKey) && e.key === "k") {
        e.preventDefault();
        setPaletteOpen((v) => !v);
      }
      if (e.key === "Escape") {
        setPaletteOpen(false);
        setCaptureOpen(false);
      }
    };
    window.addEventListener("keydown", handler);
    return () => window.removeEventListener("keydown", handler);
  }, []);

  const navItems = [
    { path: "/", label: "Tasks", icon: CheckSquare },
    { path: "/timer", label: "Focus", icon: Timer },
    { path: "/analytics", label: "Analytics", icon: BarChart3 },
  ];

  const overdueCount = tasks.filter(
    (t) => !t.completed && t.dueDate && t.dueDate < new Date()
  ).length;

  return (
    <div className="h-full w-full bg-background text-foreground flex">
      {/* Sidebar */}
      <aside className="w-64 bg-sidebar border-r border-sidebar-border flex flex-col">
        <div className="p-6 border-b border-sidebar-border">
          <div className="flex items-center gap-3">
            <div className="w-10 h-10 rounded-lg overflow-hidden flex items-center justify-center shadow-md">
              <img src="/logo.png" alt="TASKY Logo" className="w-full h-full object-cover" />
            </div>
            <div>
              <h1 className="text-xl text-sidebar-foreground">TASKY</h1>
              <p className="text-xs text-sidebar-foreground/60">Elite Productivity</p>
            </div>
          </div>
        </div>

        {/* Streak widget */}
        {streak > 0 && (
          <div className="mx-4 mt-4 px-3 py-2.5 rounded-lg bg-amber-500/10 border border-amber-500/20 flex items-center gap-2">
            <Flame className="w-4 h-4 text-amber-400 flex-shrink-0" />
            <div className="flex-1 min-w-0">
              <div className="text-sm font-semibold text-amber-400">{streak} day streak</div>
              <div className="text-[10px] text-amber-400/60">Keep it going!</div>
            </div>
          </div>
        )}

        {/* Overdue badge */}
        {overdueCount > 0 && (
          <div className="mx-4 mt-2 px-3 py-2 rounded-lg bg-destructive/10 border border-destructive/20 flex items-center justify-between">
            <span className="text-xs text-destructive font-medium">{overdueCount} overdue</span>
            <Link to="/?filter=overdue" className="text-[10px] text-destructive/70 hover:text-destructive underline">
              View
            </Link>
          </div>
        )}

        <nav className="flex-1 p-4">
          {/* Command palette trigger */}
          <button
            onClick={() => setPaletteOpen(true)}
            className="w-full flex items-center gap-3 px-4 py-2.5 mb-3 rounded-lg border border-sidebar-border text-sidebar-foreground/50 hover:text-sidebar-foreground hover:bg-sidebar-accent/30 transition-all text-sm"
          >
            <Command className="w-4 h-4" />
            <span className="flex-1 text-left">Command Palette</span>
            <kbd className="text-[10px] border border-sidebar-border rounded px-1.5">⌘K</kbd>
          </button>

          <div className="space-y-1">
            {navItems.map((item) => {
              const Icon = item.icon;
              const isActive =
                item.path === "/"
                  ? location.pathname === "/" || location.pathname === ""
                  : location.pathname.startsWith(item.path);

              return (
                <Link
                  key={item.path}
                  to={item.path}
                  className={`flex items-center gap-3 px-4 py-3 rounded-lg transition-all ${
                    isActive
                      ? "bg-sidebar-accent text-sidebar-accent-foreground"
                      : "text-sidebar-foreground/70 hover:bg-sidebar-accent/50 hover:text-sidebar-foreground"
                  }`}
                >
                  <Icon className="w-5 h-5" />
                  <span>{item.label}</span>
                </Link>
              );
            })}
          </div>
        </nav>

        <div className="p-4 border-t border-sidebar-border space-y-4">
          <button
            onClick={() => setSettingsOpen(true)}
            className="w-full flex items-center gap-3 px-4 py-2 rounded-lg text-sidebar-foreground/70 hover:bg-sidebar-accent/50 hover:text-sidebar-foreground transition-all"
            title={aiConfigured ? "Settings" : "Settings — AI key not configured"}
          >
            <div className="relative">
              <Settings className="w-4 h-4" />
              {!aiConfigured && (
                <span className="absolute -top-0.5 -right-0.5 w-2 h-2 rounded-full bg-amber-400" />
              )}
            </div>
            <span>Settings</span>
          </button>
          <button
            onClick={toggleTheme}
            className="w-full flex items-center gap-3 px-4 py-2 rounded-lg text-sidebar-foreground/70 hover:bg-sidebar-accent/50 hover:text-sidebar-foreground transition-all"
            title="Toggle Theme"
            aria-label={`Switch to ${theme === "dark" ? "light" : "dark"} mode`}
          >
            <div className="w-5 h-5 flex items-center justify-center">
              {theme === "light" ? (
                <Sun className="w-4 h-4" />
              ) : (
                <Moon className="w-4 h-4" />
              )}
            </div>
            <span className="capitalize">{theme} Mode</span>
          </button>
          <div className="text-xs text-sidebar-foreground/50 text-center">
            © 2026 TASKY
          </div>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-auto">
        <Outlet />
      </main>

      {/* Command Palette */}
      <CommandPalette
        open={paletteOpen}
        onClose={() => setPaletteOpen(false)}
        projects={projects}
        onNewTask={openNewTask}
        onToggleTheme={toggleTheme}
        onAICapture={() => {
          setPaletteOpen(false);
          setCaptureOpen(true);
        }}
        theme={theme}
      />

      {/* Settings */}
      <SettingsModal open={settingsOpen} onClose={() => setSettingsOpen(false)} />

      {/* Daily Digest */}
      <DailyDigest
        open={digestOpen}
        onClose={() => setDigestOpen(false)}
        tasks={tasks}
        streak={streak}
      />
    </div>
  );
}
