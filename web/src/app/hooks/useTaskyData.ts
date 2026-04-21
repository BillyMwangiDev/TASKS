import { useState, useEffect } from "react";
import { Task, Project, FocusSession, TaskyData } from "../types";
import { useBridge } from "./useBridge";

const STORAGE_KEY = "tasky_data";

const defaultProjects: Project[] = [
  { id: "1", name: "Personal", color: "#8b5cf6", isArchived: false },
  { id: "2", name: "Work", color: "#3b82f6", isArchived: false },
  { id: "3", name: "Learning", color: "#10b981", isArchived: false },
];

function loadLocalStorage(): TaskyData {
  try {
    const raw = localStorage.getItem(STORAGE_KEY);
    if (!raw) return { tasks: [], projects: defaultProjects, focusSessions: [] };
    const parsed = JSON.parse(raw);
    return {
      tasks: (parsed.tasks || []).map((t: any) => ({
        ...t,
        createdAt: new Date(t.createdAt),
        dueDate: t.dueDate ? new Date(t.dueDate) : undefined,
        completedAt: t.completedAt ? new Date(t.completedAt) : undefined,
      })),
      projects: (parsed.projects || defaultProjects).map((p: any) => ({
        ...p,
        isArchived: !!p.isArchived,
      })),
      focusSessions: (parsed.focusSessions || []).map((s: any) => ({
        ...s,
        startTime: new Date(s.startTime),
        endTime: new Date(s.endTime),
      })),
    };
  } catch {
    return { tasks: [], projects: defaultProjects, focusSessions: [] };
  }
}

export function useTaskyData() {
  const bridge = useBridge();
  const [data, setData] = useState<TaskyData>(loadLocalStorage);
  const [theme, setTheme] = useState<string>("dark");

  const applyTheme = (t: string | undefined) => {
    const themes = ["dark", "light", "grey"];
    themes.forEach((th) => document.documentElement.classList.remove(th));
    const active = t ?? "dark";
    document.documentElement.classList.add(active);
    setTheme(active);
  };

  const refreshData = async () => {
    const payload = await bridge.getData();
    if (!payload) return;
    applyTheme(payload.theme);
    setData({
      tasks: (payload.tasks || []).map((t: any) => ({
        ...t,
        createdAt: new Date(t.createdAt),
        dueDate: t.dueDate ? new Date(t.dueDate) : undefined,
        completedAt: t.completedAt ? new Date(t.completedAt) : undefined,
      })),
      projects: (payload.projects || []).map((p: any) => ({
        ...p,
        isArchived: !!p.isArchived,
      })),
      focusSessions: (payload.focusSessions || []).map((s: any) => ({
        ...s,
        startTime: s.startTime ? new Date(s.startTime) : new Date(),
        endTime: s.endTime ? new Date(s.endTime) : undefined,
      })),
    });
  };

  // Initial data load once bridge is ready
  useEffect(() => {
    if (bridge.isReady) refreshData();
  }, [bridge.isReady]); // eslint-disable-line react-hooks/exhaustive-deps

  // Persist to localStorage when bridge is unavailable
  useEffect(() => {
    if (!window.pybridge) {
      localStorage.setItem(STORAGE_KEY, JSON.stringify(data));
    }
  }, [data]);

  const addTask = async (task: Omit<Task, "id" | "createdAt" | "focusMinutes">) => {
    if (window.pybridge) {
      await bridge.call("addTask", bridge.jsonStringify({ ...task, dueDate: task.dueDate?.toISOString() }));
      refreshData();
    } else {
      const newTask: Task = { ...task, id: crypto.randomUUID(), createdAt: new Date(), focusMinutes: 0 };
      setData((prev) => ({ ...prev, tasks: [...prev.tasks, newTask] }));
    }
  };

  const updateTask = async (id: string, updates: Partial<Task>) => {
    if (window.pybridge) {
      await bridge.call("updateTask", id, bridge.jsonStringify(updates));
      refreshData();
    } else {
      setData((prev) => ({
        ...prev,
        tasks: prev.tasks.map((t) => (t.id === id ? { ...t, ...updates } : t)),
      }));
    }
  };

  const deleteTask = async (id: string) => {
    if (window.pybridge) {
      await bridge.call("deleteTask", id);
      refreshData();
    } else {
      setData((prev) => ({ ...prev, tasks: prev.tasks.filter((t) => t.id !== id && t.parentId !== id) }));
    }
  };

  const toggleTask = async (id: string) => {
    if (window.pybridge) {
      await bridge.call("toggleTask", id);
      refreshData();
    } else {
      setData((prev) => ({
        ...prev,
        tasks: prev.tasks.map((t) =>
          t.id === id ? { ...t, completed: !t.completed, completedAt: !t.completed ? new Date() : undefined } : t
        ),
      }));
    }
  };

  const addFocusSession = async (session: Omit<FocusSession, "id">) => {
    if (!window.pybridge) {
      const newSession: FocusSession = { ...session, id: crypto.randomUUID() };
      setData((prev) => ({ ...prev, focusSessions: [...prev.focusSessions, newSession] }));
      if (session.taskId && session.completed) {
        const minutes = Math.round(session.duration / 60);
        updateTask(session.taskId, {
          focusMinutes: (data.tasks.find((t) => t.id === session.taskId)?.focusMinutes ?? 0) + minutes,
        });
      }
    }
  };

  const addProject = async (project: Omit<Project, "id">) => {
    if (window.pybridge) {
      await bridge.call("addProject", bridge.jsonStringify(project));
      refreshData();
    } else {
      const newProject: Project = { ...project, id: crypto.randomUUID() };
      setData((prev) => ({ ...prev, projects: [...prev.projects, newProject] }));
    }
  };

  const deleteProject = async (id: string) => {
    if (window.pybridge) {
      await bridge.call("deleteProject", id);
      refreshData();
    } else {
      setData((prev) => ({
        ...prev,
        projects: prev.projects.filter((p) => p.id !== id),
        tasks: prev.tasks.map((t) => (t.projectId === id ? { ...t, projectId: undefined } : t)),
      }));
    }
  };

  const updateProject = async (id: string, updates: Partial<Project>) => {
    if (window.pybridge) {
      await bridge.call("updateProject", id, bridge.jsonStringify(updates));
      refreshData();
    } else {
      setData((prev) => ({
        ...prev,
        projects: prev.projects.map((p) => (p.id === id ? { ...p, ...updates } : p)),
      }));
    }
  };

  const toggleTheme = async () => {
    if (window.pybridge) {
      await bridge.call("toggleTheme");
      refreshData();
    } else {
      document.documentElement.classList.toggle("dark");
    }
  };

  const getAnalyticsFromBridge = async () => {
    if (!window.pybridge) return null;
    return await bridge.call<Record<string, unknown>>("getAnalytics");
  };

  return {
    tasks: data.tasks,
    projects: data.projects,
    focusSessions: data.focusSessions,
    addTask,
    updateTask,
    deleteTask,
    toggleTask,
    addFocusSession,
    addProject,
    deleteProject,
    updateProject,
    toggleTheme,
    getAnalyticsFromBridge,
    theme,
    isBridgeReady: bridge.isReady,
  };
}
