import { z } from "zod";

export const TaskSchema = z.object({
  id: z.string(),
  title: z.string(),
  description: z.string().optional().default(""),
  notes: z.string().optional().default(""),
  completed: z.boolean().default(false),
  projectId: z.string().nullable().optional(),
  tags: z.array(z.string()).default([]),
  dueDate: z.string().nullable().optional(),
  createdAt: z.string().nullable().optional(),
  completedAt: z.string().nullable().optional(),
  parentId: z.string().nullable().optional(),
  focusMinutes: z.number().default(0),
  priority: z.number().default(2),
  isRecurring: z.boolean().default(false),
  recurrenceRule: z.string().nullable().optional(),
});

export const ProjectSchema = z.object({
  id: z.string(),
  name: z.string(),
  color: z.string().default("#8b5cf6"),
  isArchived: z.boolean().default(false),
});

export const BridgePayloadSchema = z.object({
  tasks: z.array(TaskSchema),
  projects: z.array(ProjectSchema),
  focusSessions: z.array(z.any()).default([]),
  theme: z.string().optional(),
});

export type BridgePayload = z.infer<typeof BridgePayloadSchema>;
