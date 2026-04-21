import { useState } from "react";
import { useBridge } from "./useBridge";
import { Task } from "../types";

interface SubtaskSuggestion {
  title: string;
  priority: number;
  estimated_minutes: number;
}

interface CapturedTask {
  title: string;
  priority: number;
  due_date: string | null;
}

interface DigestResult {
  digest: string;
  stats: Record<string, unknown>;
}

export function useAI() {
  const bridge = useBridge();
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const isAvailable = async (): Promise<boolean> => {
    if (!window.pybridge) return false;
    const res = await bridge.call<{ available: boolean }>("isAIAvailable");
    return res?.available === true;
  };

  const breakdownTask = async (
    task: Pick<Task, "title" | "description">
  ): Promise<SubtaskSuggestion[]> => {
    setLoading(true);
    setError(null);
    try {
      const payload = bridge.jsonStringify({
        title: task.title,
        description: task.description ?? "",
      });
      const res = await bridge.call<{ subtasks: SubtaskSuggestion[] }>("aiBreakdown", payload);
      return res?.subtasks ?? [];
    } catch (e: unknown) {
      const msg = e instanceof Error ? e.message : "AI breakdown failed";
      setError(msg);
      return [];
    } finally {
      setLoading(false);
    }
  };

  const captureFromText = async (text: string): Promise<CapturedTask[]> => {
    setLoading(true);
    setError(null);
    try {
      const res = await bridge.call<{ tasks: CapturedTask[] }>("aiCapture", text);
      return res?.tasks ?? [];
    } catch (e: unknown) {
      const msg = e instanceof Error ? e.message : "AI capture failed";
      setError(msg);
      return [];
    } finally {
      setLoading(false);
    }
  };

  const getWeeklyDigest = async (): Promise<DigestResult | null> => {
    setLoading(true);
    setError(null);
    try {
      return await bridge.call<DigestResult>("aiDigest");
    } catch (e: unknown) {
      const msg = e instanceof Error ? e.message : "Digest generation failed";
      setError(msg);
      return null;
    } finally {
      setLoading(false);
    }
  };

  const getStreak = async (): Promise<number> => {
    if (!window.pybridge) return 0;
    try {
      const res = await bridge.call<{ streak: number }>("getStreak");
      return res?.streak ?? 0;
    } catch {
      return 0;
    }
  };

  return { loading, error, isAvailable, breakdownTask, captureFromText, getWeeklyDigest, getStreak };
}
