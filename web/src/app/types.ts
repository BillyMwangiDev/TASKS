export interface Task {
  id: string;
  title: string;
  description?: string;
  notes?: string;
  completed: boolean;
  projectId?: string;
  tags: string[];
  dueDate?: Date;
  createdAt: Date;
  completedAt?: Date;
  parentId?: string;
  focusMinutes: number;
  priority: number;
  isRecurring: boolean;
  recurrenceRule?: string;
}

export interface Project {
  id: string;
  name: string;
  color: string;
  isArchived: boolean;
}

export interface FocusSession {
  id: string;
  taskId?: string;
  duration: number;
  startTime: Date;
  endTime: Date;
  completed: boolean;
}

export interface TaskyData {
  tasks: Task[];
  projects: Project[];
  focusSessions: FocusSession[];
}
