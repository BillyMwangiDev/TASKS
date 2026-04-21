import { useMemo } from "react";
import { Task } from "../types";
import { format } from "date-fns";
import { Flame, CheckSquare, AlertCircle, X, Calendar } from "lucide-react";
import { motion, AnimatePresence } from "motion/react";

interface DailyDigestProps {
  open: boolean;
  onClose: () => void;
  tasks: Task[];
  streak: number;
}

export function DailyDigest({ open, onClose, tasks, streak }: DailyDigestProps) {
  const today = new Date();

  const stats = useMemo(() => {
    const overdue = tasks.filter(
      (t) => !t.completed && t.dueDate && t.dueDate < today
    );
    const dueToday = tasks.filter(
      (t) =>
        !t.completed &&
        t.dueDate &&
        t.dueDate.toDateString() === today.toDateString()
    );
    const highPriority = tasks.filter(
      (t) => !t.completed && t.priority === 1
    );
    const completedToday = tasks.filter(
      (t) =>
        t.completed &&
        t.completedAt &&
        t.completedAt.toDateString() === today.toDateString()
    );
    return { overdue, dueToday, highPriority, completedToday };
  }, [tasks]); // eslint-disable-line react-hooks/exhaustive-deps

  const greeting = () => {
    const h = today.getHours();
    if (h < 12) return "Good morning";
    if (h < 18) return "Good afternoon";
    return "Good evening";
  };

  return (
    <AnimatePresence>
      {open && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            exit={{ opacity: 0 }}
            className="absolute inset-0 bg-black/50 backdrop-blur-sm"
            onClick={onClose}
          />
          <motion.div
            initial={{ opacity: 0, scale: 0.95, y: 20 }}
            animate={{ opacity: 1, scale: 1, y: 0 }}
            exit={{ opacity: 0, scale: 0.95, y: 20 }}
            transition={{ type: "spring", duration: 0.4 }}
            className="relative w-full max-w-md bg-card border border-border rounded-2xl shadow-2xl overflow-hidden"
          >
            {/* Header gradient */}
            <div className="px-6 pt-6 pb-4 bg-gradient-to-br from-primary/10 to-violet-500/5">
              <div className="flex items-start justify-between">
                <div>
                  <p className="text-sm text-muted-foreground">{format(today, "EEEE, MMMM d")}</p>
                  <h2 className="text-xl font-semibold mt-0.5">{greeting()}</h2>
                </div>
                <button
                  onClick={onClose}
                  className="p-1.5 hover:bg-accent rounded-lg text-muted-foreground hover:text-foreground transition-colors"
                >
                  <X className="w-4 h-4" />
                </button>
              </div>

              {streak > 0 && (
                <div className="mt-3 flex items-center gap-2 px-3 py-2 bg-amber-500/10 border border-amber-500/20 rounded-lg w-fit">
                  <Flame className="w-4 h-4 text-amber-400" />
                  <span className="text-sm font-medium text-amber-400">{streak} day streak</span>
                </div>
              )}
            </div>

            {/* Stats */}
            <div className="p-6 grid grid-cols-2 gap-3">
              <StatCard
                icon={<AlertCircle className="w-4 h-4" />}
                label="Overdue"
                count={stats.overdue.length}
                color={stats.overdue.length > 0 ? "text-destructive" : "text-muted-foreground"}
                bgColor={stats.overdue.length > 0 ? "bg-destructive/10" : "bg-muted/30"}
              />
              <StatCard
                icon={<Calendar className="w-4 h-4" />}
                label="Due Today"
                count={stats.dueToday.length}
                color={stats.dueToday.length > 0 ? "text-primary" : "text-muted-foreground"}
                bgColor={stats.dueToday.length > 0 ? "bg-primary/10" : "bg-muted/30"}
              />
              <StatCard
                icon={<CheckSquare className="w-4 h-4" />}
                label="Done Today"
                count={stats.completedToday.length}
                color="text-emerald-500"
                bgColor="bg-emerald-500/10"
              />
              <StatCard
                icon={<AlertCircle className="w-4 h-4" />}
                label="High Priority"
                count={stats.highPriority.length}
                color={stats.highPriority.length > 0 ? "text-red-500" : "text-muted-foreground"}
                bgColor={stats.highPriority.length > 0 ? "bg-red-500/10" : "bg-muted/30"}
              />
            </div>

            {/* Top tasks for today */}
            {stats.dueToday.length > 0 && (
              <div className="px-6 pb-4">
                <p className="text-xs font-medium text-muted-foreground uppercase tracking-wider mb-2">
                  Focus on today
                </p>
                <div className="space-y-1.5">
                  {stats.dueToday.slice(0, 3).map((t) => (
                    <div key={t.id} className="flex items-center gap-2 px-3 py-2 bg-muted/30 rounded-lg">
                      <div
                        className={`w-2 h-2 rounded-full flex-shrink-0 ${
                          t.priority === 1 ? "bg-red-500" : t.priority === 2 ? "bg-amber-500" : "bg-blue-500"
                        }`}
                      />
                      <span className="text-sm truncate">{t.title}</span>
                    </div>
                  ))}
                  {stats.dueToday.length > 3 && (
                    <p className="text-xs text-muted-foreground pl-3">
                      +{stats.dueToday.length - 3} more
                    </p>
                  )}
                </div>
              </div>
            )}

            {/* CTA */}
            <div className="px-6 pb-6">
              <button
                onClick={onClose}
                className="w-full py-2.5 bg-primary text-primary-foreground rounded-xl text-sm font-medium hover:bg-primary/90 transition-colors"
              >
                Let's get to work
              </button>
            </div>
          </motion.div>
        </div>
      )}
    </AnimatePresence>
  );
}

function StatCard({
  icon,
  label,
  count,
  color,
  bgColor,
}: {
  icon: React.ReactNode;
  label: string;
  count: number;
  color: string;
  bgColor: string;
}) {
  return (
    <div className={`${bgColor} rounded-xl p-4`}>
      <div className={`${color} flex items-center gap-1.5 mb-1`}>
        {icon}
        <span className="text-xs font-medium">{label}</span>
      </div>
      <span className={`text-2xl font-bold ${color}`}>{count}</span>
    </div>
  );
}
