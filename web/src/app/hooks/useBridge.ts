import { useState, useEffect, useCallback } from "react";
import { Task, Project, FocusSession, TaskyData } from "../types";
import { BridgePayloadSchema } from "./schemas";

declare global {
  interface Window {
    qt?: any;
    pybridge?: any;
  }
}

function parseDateFields(tasks: any[]): Task[] {
  return tasks.map((t) => ({
    ...t,
    createdAt: t.createdAt ? new Date(t.createdAt) : new Date(),
    dueDate: t.dueDate ? new Date(t.dueDate) : undefined,
    completedAt: t.completedAt ? new Date(t.completedAt) : undefined,
  }));
}

function jsonStringify(obj: any): string {
  return JSON.stringify(obj, (_key, value) =>
    value instanceof Date ? value.toISOString() : value
  );
}

export function useBridge() {
  const [isReady, setIsReady] = useState(false);

  useEffect(() => {
    if (typeof window.qt !== "undefined") {
      new (window as any).QWebChannel(
        window.qt.webChannelTransport,
        (channel: any) => {
          window.pybridge = channel.objects.pybridge;
          setIsReady(true);
        }
      );
    }
  }, []);

  const call = useCallback(
    async <T>(method: string, ...args: any[]): Promise<T | null> => {
      if (!window.pybridge) return null;
      try {
        const raw: string = await window.pybridge[method](...args);
        const envelope = JSON.parse(raw);
        if (!envelope.ok) {
          console.error(`[bridge] ${method} error:`, envelope.error);
          return null;
        }
        return envelope.data as T;
      } catch (err) {
        console.error(`[bridge] ${method} threw:`, err);
        return null;
      }
    },
    []
  );

  const getData = useCallback(async (): Promise<{
    tasks: Task[];
    projects: Project[];
    focusSessions: FocusSession[];
    theme?: string;
  } | null> => {
    if (!window.pybridge) return null;
    try {
      const raw: string = await window.pybridge.getData();
      const envelope = JSON.parse(raw);
      if (!envelope.ok) {
        console.error("[bridge] getData error:", envelope.error);
        return null;
      }
      const result = BridgePayloadSchema.safeParse(envelope.data);
      if (!result.success) {
        console.error("[bridge] getData schema validation failed:", result.error.flatten());
        return null;
      }
      return {
        tasks: parseDateFields(result.data.tasks),
        projects: result.data.projects,
        focusSessions: result.data.focusSessions,
        theme: result.data.theme,
      };
    } catch (err) {
      console.error("[bridge] getData threw:", err);
      return null;
    }
  }, []);

  return { isReady, call, getData, jsonStringify };
}
