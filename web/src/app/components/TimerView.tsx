import { useState, useEffect, useRef } from "react";
import { useLocation } from "react-router";
import { useTaskyData } from "../hooks/useTaskyData";
import { Play, Pause, RotateCcw, CheckCircle2, Circle } from "lucide-react";

const POMODORO_DURATION = 25 * 60; // 25 minutes
const SHORT_BREAK = 5 * 60; // 5 minutes
const LONG_BREAK = 15 * 60; // 15 minutes

type TimerMode = "focus" | "shortBreak" | "longBreak";

export function TimerView() {
  const { tasks, addFocusSession } = useTaskyData();
  const location = useLocation();
  const queryParams = new URLSearchParams(location.search);
  const initialTaskId = queryParams.get("taskId") || "";
  
  const [selectedTaskId, setSelectedTaskId] = useState<string>(initialTaskId);
  const [mode, setMode] = useState<TimerMode>("focus");
  const [timeLeft, setTimeLeft] = useState(POMODORO_DURATION);
  const [isRunning, setIsRunning] = useState(false);
  const [sessionsCompleted, setSessionsCompleted] = useState(0);
  const startTimeRef = useRef<Date | null>(null);
  const intervalRef = useRef<number | null>(null);

  const activeTasks = tasks.filter((t) => !t.completed && !t.parentId);
  const selectedTask = tasks.find((t) => t.id === selectedTaskId);

  // Auto-select task from URL if it changes
  useEffect(() => {
    if (initialTaskId && tasks.length > 0) {
      setSelectedTaskId(initialTaskId);
    }
  }, [initialTaskId, tasks]);

  const getDuration = (mode: TimerMode) => {
    switch (mode) {
      case "focus":
        return POMODORO_DURATION;
      case "shortBreak":
        return SHORT_BREAK;
      case "longBreak":
        return LONG_BREAK;
    }
  };

  useEffect(() => {
    if (isRunning) {
      intervalRef.current = window.setInterval(() => {
        setTimeLeft((prev) => {
          if (prev <= 1) {
            handleTimerComplete();
            return 0;
          }
          return prev - 1;
        });
      }, 1000);
    } else {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    }

    return () => {
      if (intervalRef.current) {
        clearInterval(intervalRef.current);
      }
    };
  }, [isRunning]);

  const handleTimerComplete = () => {
    setIsRunning(false);

    if (mode === "focus" && startTimeRef.current) {
      const endTime = new Date();
      const duration = Math.floor((endTime.getTime() - startTimeRef.current.getTime()) / 1000);

      addFocusSession({
        taskId: selectedTaskId || undefined,
        duration,
        startTime: startTimeRef.current,
        endTime,
        completed: true,
      });

      setSessionsCompleted((prev) => prev + 1);

      // Show notification
      if ("Notification" in window && Notification.permission === "granted") {
        new Notification("TASKY - Focus Session Complete! 🎉", {
          body: selectedTask
            ? `Great work on "${selectedTask.title}"!`
            : "Time for a break!",
        });
      }

      // Auto-switch to break
      const nextMode = (sessionsCompleted + 1) % 4 === 0 ? "longBreak" : "shortBreak";
      setMode(nextMode);
      setTimeLeft(getDuration(nextMode));
    } else if (mode !== "focus") {
      // Break complete
      if ("Notification" in window && Notification.permission === "granted") {
        new Notification("TASKY - Break Complete! 💪", {
          body: "Ready to focus again?",
        });
      }
      setMode("focus");
      setTimeLeft(POMODORO_DURATION);
    }
  };

  const handleStart = () => {
    if (!isRunning) {
      startTimeRef.current = new Date();
      setIsRunning(true);

      // Request notification permission
      if ("Notification" in window && Notification.permission === "default") {
        Notification.requestPermission();
      }
    }
  };

  const handlePause = () => {
    setIsRunning(false);
    if (startTimeRef.current && mode === "focus") {
      const endTime = new Date();
      const duration = Math.floor((endTime.getTime() - startTimeRef.current.getTime()) / 1000);

      addFocusSession({
        taskId: selectedTaskId || undefined,
        duration,
        startTime: startTimeRef.current,
        endTime,
        completed: false,
      });
    }
    startTimeRef.current = null;
  };

  const handleReset = () => {
    setIsRunning(false);
    setTimeLeft(getDuration(mode));
    startTimeRef.current = null;
  };

  const handleModeChange = (newMode: TimerMode) => {
    setMode(newMode);
    setTimeLeft(getDuration(newMode));
    setIsRunning(false);
    startTimeRef.current = null;
  };

  const formatTime = (seconds: number) => {
    const mins = Math.floor(seconds / 60);
    const secs = seconds % 60;
    return `${mins.toString().padStart(2, "0")}:${secs.toString().padStart(2, "0")}`;
  };

  const progress = ((getDuration(mode) - timeLeft) / getDuration(mode)) * 100;

  return (
    <div className="h-full flex flex-col items-center justify-center bg-gradient-to-br from-background to-muted/20 p-8">
      <div className="w-full max-w-2xl">
        {/* Mode Selector */}
        <div className="flex gap-2 mb-8 bg-card border border-border rounded-lg p-2">
          {(["focus", "shortBreak", "longBreak"] as TimerMode[]).map((m) => (
            <button
              key={m}
              onClick={() => handleModeChange(m)}
              disabled={isRunning}
              className={`flex-1 py-2 px-4 rounded-md transition-all ${
                mode === m
                  ? "bg-primary text-primary-foreground"
                  : "hover:bg-accent text-muted-foreground"
              } ${isRunning ? "opacity-50 cursor-not-allowed" : ""}`}
            >
              {m === "focus" ? "Focus (25m)" : m === "shortBreak" ? "Short Break (5m)" : "Long Break (15m)"}
            </button>
          ))}
        </div>

        {/* Timer Display */}
        <div className="bg-card border border-border rounded-2xl p-12 mb-8 relative overflow-hidden">
          {/* Progress Ring Background */}
          <div className="absolute inset-0 opacity-10">
            <svg className="w-full h-full transform -rotate-90">
              <circle
                cx="50%"
                cy="50%"
                r="45%"
                fill="none"
                stroke="currentColor"
                strokeWidth="8"
                className="text-primary"
                strokeDasharray={`${progress * 2.827} 282.7`}
              />
            </svg>
          </div>

          <div className="relative text-center">
            <div className="text-8xl mb-6 font-mono tracking-wider">{formatTime(timeLeft)}</div>

            {mode === "focus" && (
              <div className="mb-6">
                <label htmlFor="focus-task-select" className="block text-sm text-muted-foreground mb-2">Focus on:</label>
                <select
                  id="focus-task-select"
                  aria-label="Select task for focus session"
                  value={selectedTaskId}
                  onChange={(e) => setSelectedTaskId(e.target.value)}
                  disabled={isRunning}
                  className="px-4 py-2 bg-input-background border border-border rounded-lg text-center disabled:opacity-50 disabled:cursor-not-allowed min-w-[300px]"
                >
                  <option value="">General Focus Session</option>
                  {activeTasks.map((task) => (
                    <option key={task.id} value={task.id}>
                      {task.title}
                    </option>
                  ))}
                </select>
              </div>
            )}

            {/* Control Buttons */}
            <div className="flex gap-4 justify-center">
              {!isRunning ? (
                <button
                  onClick={handleStart}
                  className="w-16 h-16 rounded-full bg-primary text-primary-foreground hover:opacity-90 transition-all flex items-center justify-center shadow-lg hover:shadow-xl"
                >
                  <Play className="w-8 h-8" />
                </button>
              ) : (
                <button
                  onClick={handlePause}
                  className="w-16 h-16 rounded-full bg-primary text-primary-foreground hover:opacity-90 transition-all flex items-center justify-center shadow-lg hover:shadow-xl"
                >
                  <Pause className="w-8 h-8" />
                </button>
              )}
              <button
                onClick={handleReset}
                className="w-16 h-16 rounded-full bg-secondary text-secondary-foreground hover:bg-secondary/80 transition-all flex items-center justify-center"
              >
                <RotateCcw className="w-6 h-6" />
              </button>
            </div>
          </div>
        </div>

        {/* Session Counter */}
        <div className="bg-card border border-border rounded-lg p-6">
          <div className="flex items-center justify-between mb-4">
            <h3>Sessions Today</h3>
            <span className="text-2xl">{sessionsCompleted}</span>
          </div>
          <div className="flex gap-2">
            {Array.from({ length: 8 }).map((_, i) => (
              <div
                key={i}
                className={`flex-1 h-2 rounded-full ${
                  i < sessionsCompleted ? "bg-primary" : "bg-muted"
                }`}
              />
            ))}
          </div>
          <p className="text-xs text-muted-foreground mt-3 text-center">
            {sessionsCompleted > 0
              ? `${sessionsCompleted * 25} minutes of deep focus! Keep going! 🔥`
              : "Start your first session to build momentum"}
          </p>
        </div>

        {/* Selected Task Info */}
        {selectedTask && mode === "focus" && (
          <div className="mt-6 bg-card border border-border rounded-lg p-4">
            <div className="flex items-start gap-3">
              <CheckCircle2 className="w-5 h-5 text-primary mt-0.5" />
              <div className="flex-1">
                <h4 className="mb-1">{selectedTask.title}</h4>
                <p className="text-sm text-muted-foreground">
                  {selectedTask.focusMinutes > 0
                    ? `${selectedTask.focusMinutes} minutes focused so far`
                    : "First focus session on this task"}
                </p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
