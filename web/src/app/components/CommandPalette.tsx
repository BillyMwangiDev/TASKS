import { useEffect, useState } from "react";
import { useNavigate } from "react-router";
import { Command } from "cmdk";
import {
  CheckSquare,
  Timer,
  BarChart3,
  Plus,
  Search,
  Sun,
  Moon,
  Sparkles,
  Folder,
  Zap,
} from "lucide-react";
import { Project } from "../types";

interface CommandPaletteProps {
  open: boolean;
  onClose: () => void;
  projects: Project[];
  onNewTask: () => void;
  onToggleTheme: () => void;
  onAICapture: () => void;
  theme: string;
}

export function CommandPalette({
  open,
  onClose,
  projects,
  onNewTask,
  onToggleTheme,
  onAICapture,
  theme,
}: CommandPaletteProps) {
  const navigate = useNavigate();
  const [search, setSearch] = useState("");

  // Reset search when closed
  useEffect(() => {
    if (!open) setSearch("");
  }, [open]);

  const run = (fn: () => void) => {
    fn();
    onClose();
  };

  if (!open) return null;

  return (
    <div
      className="fixed inset-0 z-50 flex items-start justify-center pt-[15vh]"
      onClick={onClose}
    >
      {/* Backdrop */}
      <div className="absolute inset-0 bg-black/50 backdrop-blur-sm" />

      {/* Panel */}
      <div
        className="relative w-full max-w-xl mx-4 rounded-xl border border-border bg-card shadow-2xl overflow-hidden"
        onClick={(e) => e.stopPropagation()}
      >
        <Command className="[&_[cmdk-input-wrapper]]:border-b [&_[cmdk-input-wrapper]]:border-border">
          <div className="flex items-center gap-3 px-4 py-3">
            <Search className="w-4 h-4 text-muted-foreground flex-shrink-0" />
            <Command.Input
              value={search}
              onValueChange={setSearch}
              placeholder="Type a command or search..."
              className="flex-1 bg-transparent outline-none text-sm placeholder:text-muted-foreground"
              autoFocus
            />
            <kbd className="text-[10px] text-muted-foreground border border-border rounded px-1.5 py-0.5">
              ESC
            </kbd>
          </div>

          <Command.List className="max-h-80 overflow-y-auto p-2">
            <Command.Empty className="py-8 text-center text-sm text-muted-foreground">
              No results found.
            </Command.Empty>

            <Command.Group heading="Actions" className="[&_[cmdk-group-heading]]:px-2 [&_[cmdk-group-heading]]:py-1 [&_[cmdk-group-heading]]:text-[10px] [&_[cmdk-group-heading]]:uppercase [&_[cmdk-group-heading]]:tracking-wider [&_[cmdk-group-heading]]:text-muted-foreground">
              <PaletteItem
                icon={<Plus className="w-4 h-4" />}
                label="New Task"
                shortcut="N"
                onSelect={() => run(onNewTask)}
              />
              <PaletteItem
                icon={<Sparkles className="w-4 h-4 text-violet-400" />}
                label="AI Capture from Text"
                description="Paste notes → extract tasks"
                onSelect={() => run(onAICapture)}
              />
              <PaletteItem
                icon={theme === "dark" ? <Sun className="w-4 h-4" /> : <Moon className="w-4 h-4" />}
                label="Toggle Theme"
                shortcut="T"
                onSelect={() => run(onToggleTheme)}
              />
            </Command.Group>

            <Command.Group heading="Navigate" className="[&_[cmdk-group-heading]]:px-2 [&_[cmdk-group-heading]]:py-1 [&_[cmdk-group-heading]]:text-[10px] [&_[cmdk-group-heading]]:uppercase [&_[cmdk-group-heading]]:tracking-wider [&_[cmdk-group-heading]]:text-muted-foreground">
              <PaletteItem
                icon={<CheckSquare className="w-4 h-4" />}
                label="Go to Tasks"
                onSelect={() => run(() => navigate("/"))}
              />
              <PaletteItem
                icon={<Timer className="w-4 h-4" />}
                label="Go to Focus Timer"
                onSelect={() => run(() => navigate("/timer"))}
              />
              <PaletteItem
                icon={<BarChart3 className="w-4 h-4" />}
                label="Go to Analytics"
                onSelect={() => run(() => navigate("/analytics"))}
              />
            </Command.Group>

            {projects.filter((p) => !p.isArchived).length > 0 && (
              <Command.Group heading="Projects" className="[&_[cmdk-group-heading]]:px-2 [&_[cmdk-group-heading]]:py-1 [&_[cmdk-group-heading]]:text-[10px] [&_[cmdk-group-heading]]:uppercase [&_[cmdk-group-heading]]:tracking-wider [&_[cmdk-group-heading]]:text-muted-foreground">
                {projects
                  .filter((p) => !p.isArchived)
                  .map((p) => (
                    <PaletteItem
                      key={p.id}
                      icon={
                        <div
                          className="w-4 h-4 rounded-full flex-shrink-0"
                          style={{ backgroundColor: p.color }}
                        />
                      }
                      label={p.name}
                      onSelect={() =>
                        run(() => navigate(`/?project=${p.id}`))
                      }
                    />
                  ))}
              </Command.Group>
            )}

            <Command.Group heading="AI Features" className="[&_[cmdk-group-heading]]:px-2 [&_[cmdk-group-heading]]:py-1 [&_[cmdk-group-heading]]:text-[10px] [&_[cmdk-group-heading]]:uppercase [&_[cmdk-group-heading]]:tracking-wider [&_[cmdk-group-heading]]:text-muted-foreground">
              <PaletteItem
                icon={<Zap className="w-4 h-4 text-amber-400" />}
                label="AI Weekly Digest"
                description="Get your productivity insight"
                onSelect={() => run(() => navigate("/analytics?digest=1"))}
              />
              <PaletteItem
                icon={<Folder className="w-4 h-4 text-blue-400" />}
                label="TASKY on Claude Desktop"
                description="Use MCP to manage tasks via chat"
                onSelect={() => run(() => navigate("/analytics"))}
              />
            </Command.Group>
          </Command.List>

          <div className="border-t border-border px-4 py-2 flex items-center gap-4 text-[10px] text-muted-foreground">
            <span><kbd className="border border-border rounded px-1">↑↓</kbd> navigate</span>
            <span><kbd className="border border-border rounded px-1">↵</kbd> select</span>
            <span><kbd className="border border-border rounded px-1">ESC</kbd> close</span>
          </div>
        </Command>
      </div>
    </div>
  );
}

function PaletteItem({
  icon,
  label,
  description,
  shortcut,
  onSelect,
}: {
  icon: React.ReactNode;
  label: string;
  description?: string;
  shortcut?: string;
  onSelect: () => void;
}) {
  return (
    <Command.Item
      onSelect={onSelect}
      className="flex items-center gap-3 px-3 py-2.5 rounded-lg cursor-pointer text-sm
        data-[selected=true]:bg-accent data-[selected=true]:text-accent-foreground
        hover:bg-accent/50 transition-colors"
    >
      <span className="text-muted-foreground flex-shrink-0">{icon}</span>
      <span className="flex-1 font-medium">{label}</span>
      {description && (
        <span className="text-xs text-muted-foreground">{description}</span>
      )}
      {shortcut && (
        <kbd className="text-[10px] border border-border rounded px-1.5 py-0.5 text-muted-foreground">
          {shortcut}
        </kbd>
      )}
    </Command.Item>
  );
}
