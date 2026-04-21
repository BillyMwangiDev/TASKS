import { useState, useMemo } from "react";
import { useNavigate } from "react-router";
import { useTaskyData } from "../hooks/useTaskyData";
import { useAI } from "../hooks/useAI";
import { Task } from "../types";
import {
  Plus,
  Search,
  ChevronRight,
  ChevronDown,
  Check,
  Trash2,
  Tag,
  Calendar,
  Clock,
  CheckSquare,
  AlertCircle,
  Flag,
  FileText,
  RotateCw,
  Play,
  Filter,
  ArrowUpDown,
  Archive,
  ArchiveRestore,
  Sparkles,
  Loader2,
  X,
  ClipboardPaste,
} from "lucide-react";
import { format } from "date-fns";
import confetti from "canvas-confetti";
import { motion, AnimatePresence } from "motion/react";
import { parseNaturalDate } from "../utils/naturalDate";

export function TasksView() {
  const {
    tasks,
    projects,
    addTask,
    updateTask,
    deleteTask,
    toggleTask,
    addProject,
    deleteProject,
    updateProject,
  } = useTaskyData();
  const { breakdownTask, captureFromText, loading: aiLoading, error: aiError } = useAI();

  const handleToggleTask = (taskId: string) => {
    const task = tasks.find(t => t.id === taskId);
    if (task && !task.completed) {
      confetti({
        particleCount: 100,
        spread: 70,
        origin: { y: 0.6 },
        colors: ["#3b82f6", "#60a5fa", "#10b981"],
      });
    }
    toggleTask(taskId);
  };

  const [newTaskTitle, setNewTaskTitle] = useState("");
  const [selectedProject, setSelectedProject] = useState<string>("");
  const [searchQuery, setSearchQuery] = useState("");
  const [hideCompleted, setHideCompleted] = useState(false);
  const [showArchivedProjects, setShowArchivedProjects] = useState(false);
  const [sortBy, setSortBy] = useState<"date" | "priority" | "title">("date");
  const [expandedTasks, setExpandedTasks] = useState<Set<string>>(new Set());
  const [showNewProject, setShowNewProject] = useState(false);
  const [newProjectName, setNewProjectName] = useState("");
  const [newProjectColor, setNewProjectColor] = useState("#3b82f6");
  const [newTaskPriority, setNewTaskPriority] = useState(2);
  const [selectedTaskIds, setSelectedTaskIds] = useState<Set<string>>(new Set());
  const [captureText, setCaptureText] = useState("");
  const [showCapture, setShowCapture] = useState(false);
  const [capturedTasks, setCapturedTasks] = useState<Array<{ title: string; priority: number; due_date: string | null }>>([]);
  const [naturalDateInput, setNaturalDateInput] = useState("");
  const navigate = useNavigate();

  const getSubtasks = (parentId: string) => {
    return tasks.filter((t) => t.parentId === parentId);
  };

  const sortedAndFilteredTasks = useMemo(() => {
    let result = tasks.filter((t) => !t.parentId);

    // Filter
    if (selectedProject) result = result.filter((t) => t.projectId === selectedProject);
    if (searchQuery) result = result.filter((t) => t.title.toLowerCase().includes(searchQuery.toLowerCase()));
    if (hideCompleted) result = result.filter((t) => !t.completed);

    // Sort
    result.sort((a, b) => {
      if (sortBy === "priority") return a.priority - b.priority;
      if (sortBy === "title") return a.title.localeCompare(b.title);
      // Default: date (newest first)
      return new Date(b.createdAt).getTime() - new Date(a.createdAt).getTime();
    });

    return result;
  }, [tasks, selectedProject, searchQuery, hideCompleted, sortBy]);

  const handleAddTask = (parentId?: string) => {
    if (!newTaskTitle.trim()) return;
    const parsedDue = naturalDateInput ? parseNaturalDate(naturalDateInput) : undefined;
    addTask({
      title: newTaskTitle,
      completed: false,
      tags: [],
      parentId,
      projectId: selectedProject || undefined,
      priority: newTaskPriority,
      isRecurring: false,
      dueDate: parsedDue ?? undefined,
    });
    setNewTaskTitle("");
    setNewTaskPriority(2);
    setNaturalDateInput("");
  };

  const toggleExpanded = (taskId: string) => {
    setExpandedTasks((prev) => {
      const next = new Set(prev);
      if (next.has(taskId)) {
        next.delete(taskId);
      } else {
        next.add(taskId);
      }
      return next;
    });
  };

  const handleAddProject = () => {
    if (!newProjectName.trim()) return;
    addProject({
      name: newProjectName,
      color: newProjectColor,
      isArchived: false,
    });
    setNewProjectName("");
    setNewProjectColor("#3b82f6");
    setShowNewProject(false);
  };
  
  const toggleSelectTask = (taskId: string) => {
    setSelectedTaskIds(prev => {
      const next = new Set(prev);
      if (next.has(taskId)) next.delete(taskId);
      else next.add(taskId);
      return next;
    });
  };

  const handleBulkDelete = () => {
    if (confirm(`Delete ${selectedTaskIds.size} tasks?`)) {
      selectedTaskIds.forEach(id => deleteTask(id));
      setSelectedTaskIds(new Set());
    }
  };

  const handleBulkToggle = () => {
    selectedTaskIds.forEach(id => toggleTask(id));
    setSelectedTaskIds(new Set());
  };

  const handleAICapture = async () => {
    if (!captureText.trim()) return;
    const results = await captureFromText(captureText);
    setCapturedTasks(results);
  };

  const acceptCapturedTasks = () => {
    capturedTasks.forEach((ct) => {
      addTask({
        title: ct.title,
        completed: false,
        tags: [],
        priority: ct.priority ?? 2,
        projectId: selectedProject || undefined,
        isRecurring: false,
        dueDate: ct.due_date ? new Date(ct.due_date) : undefined,
      });
    });
    setCapturedTasks([]);
    setCaptureText("");
    setShowCapture(false);
  };

  const isOverdue = (task: Task): boolean => {
    return !!(task.dueDate && !task.completed && task.dueDate < new Date());
  };

  return (
    <div className="h-full flex flex-col">
      {/* Header */}
      <div className="border-b border-border bg-card">
        <div className="p-6">
          <div className="flex items-center justify-between mb-4">
            <h2>Task Management</h2>
            <button
              onClick={() => setShowCapture(!showCapture)}
              className={`flex items-center gap-2 px-3 py-1.5 rounded-lg text-sm transition-all ${
                showCapture
                  ? "bg-blue-500 text-white"
                  : "border border-border hover:bg-accent text-muted-foreground hover:text-foreground"
              }`}
              title="Paste notes or text to extract tasks with AI"
            >
              <Sparkles className="w-4 h-4" />
              AI Capture
            </button>
          </div>

          {/* AI Capture Panel */}
          <AnimatePresence>
            {showCapture && (
              <motion.div
                initial={{ opacity: 0, height: 0 }}
                animate={{ opacity: 1, height: "auto" }}
                exit={{ opacity: 0, height: 0 }}
                className="mb-4 bg-blue-500/5 border border-blue-500/20 rounded-xl p-4 overflow-hidden"
              >
                <div className="flex items-center gap-2 mb-3">
                  <ClipboardPaste className="w-4 h-4 text-blue-400" />
                  <span className="text-sm font-medium text-blue-400">AI Task Capture</span>
                  <span className="text-xs text-muted-foreground ml-1">
                    Paste emails, meeting notes, or any text — Claude extracts the action items.
                  </span>
                </div>
                <textarea
                  value={captureText}
                  onChange={(e) => setCaptureText(e.target.value)}
                  placeholder="Paste your notes, email, or meeting transcript here..."
                  className="w-full bg-input-background px-3 py-2 rounded-lg border border-border text-sm min-h-[100px] resize-none mb-3"
                />
                {capturedTasks.length > 0 ? (
                  <div className="space-y-2 mb-3">
                    <p className="text-xs text-muted-foreground font-medium">Found {capturedTasks.length} action items:</p>
                    {capturedTasks.map((ct, i) => (
                      <div key={i} className="flex items-center gap-2 px-3 py-2 bg-card rounded-lg border border-border">
                        <div className={`w-2 h-2 rounded-full flex-shrink-0 ${ct.priority === 1 ? "bg-red-500" : ct.priority === 2 ? "bg-amber-500" : "bg-blue-500"}`} />
                        <span className="flex-1 text-sm">{ct.title}</span>
                        {ct.due_date && (
                          <span className="text-xs text-muted-foreground">{format(new Date(ct.due_date), "MMM d")}</span>
                        )}
                        <button onClick={() => setCapturedTasks((prev) => prev.filter((_, j) => j !== i))} className="text-muted-foreground hover:text-destructive">
                          <X className="w-3 h-3" />
                        </button>
                      </div>
                    ))}
                    <div className="flex gap-2 pt-1">
                      <button onClick={acceptCapturedTasks} className="flex-1 px-3 py-1.5 bg-blue-500 text-white rounded-lg text-sm hover:bg-blue-600 transition-colors">
                        Add All Tasks
                      </button>
                      <button onClick={() => setCapturedTasks([])} className="px-3 py-1.5 bg-secondary text-secondary-foreground rounded-lg text-sm">
                        Discard
                      </button>
                    </div>
                  </div>
                ) : (
                  <button
                    onClick={handleAICapture}
                    disabled={aiLoading || !captureText.trim()}
                    className="flex items-center gap-2 px-4 py-2 bg-blue-500 text-white rounded-lg text-sm hover:bg-blue-600 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
                  >
                    {aiLoading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Sparkles className="w-4 h-4" />}
                    {aiLoading ? "Extracting…" : "Extract Tasks"}
                  </button>
                )}
                {aiError && <p className="text-xs text-destructive mt-2">{aiError}</p>}
              </motion.div>
            )}
          </AnimatePresence>

          <div className="flex flex-wrap gap-3 items-center">
            <div className="flex-1 relative min-w-[200px]">
              <Search className="absolute left-3 top-1/2 -translate-y-1/2 w-5 h-5 text-muted-foreground" />
              <input
                type="text"
                placeholder="Search tasks..."
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                className="w-full pl-10 pr-4 py-2 bg-input-background rounded-lg border border-border focus:outline-none focus:ring-2 focus:ring-ring"
              />
            </div>
            
            <div className="flex items-center gap-2">
              <button
                onClick={() => setHideCompleted(!hideCompleted)}
                className={`flex items-center gap-2 px-3 py-2 rounded-lg border transition-all ${
                  hideCompleted ? "bg-primary/10 border-primary text-primary" : "border-border hover:bg-accent"
                }`}
              >
                <Filter className="w-4 h-4" />
                <span className="text-sm">{hideCompleted ? "Show Completed" : "Hide Completed"}</span>
              </button>

              <div className="flex items-center gap-2 bg-card border border-border rounded-lg px-2 py-1">
                <ArrowUpDown className="w-4 h-4 text-muted-foreground" />
                <select 
                  value={sortBy}
                  onChange={(e) => setSortBy(e.target.value as any)}
                  className="bg-transparent text-sm border-none focus:ring-0 outline-none"
                >
                  <option value="date">Newest</option>
                  <option value="priority">Priority</option>
                  <option value="title">A-Z</option>
                </select>
              </div>
            </div>
          </div>
        </div>
      </div>

      <div className="flex-1 flex overflow-hidden">
        {/* Sidebar Projects */}
        <div className="w-64 border-r border-border bg-card p-4 overflow-auto">
          <div className="mb-4">
            <h3 className="mb-3 text-muted-foreground">Projects</h3>
            <button
              onClick={() => setSelectedProject("")}
              className={`w-full text-left px-3 py-2 rounded-lg mb-1 transition-colors ${
                selectedProject === ""
                  ? "bg-accent text-accent-foreground"
                  : "hover:bg-accent/50"
              }`}
            >
              All Tasks
            </button>
            {projects.filter(p => showArchivedProjects ? true : !p.isArchived).map((project) => (
              <div key={project.id} className="relative group">
                <button
                  onClick={() => setSelectedProject(project.id)}
                  className={`w-full text-left px-3 py-2 rounded-lg mb-1 transition-colors flex items-center gap-2 ${
                    selectedProject === project.id
                      ? "bg-accent text-accent-foreground"
                      : "hover:bg-accent/50"
                  } ${project.isArchived ? "opacity-50 grayscale" : ""}`}
                >
                  <div
                    className="w-4 h-4 rounded-full flex-shrink-0"
                    style={{ backgroundColor: project.color }}
                  />
                  <span className="flex-1 truncate pr-6" title={project.name}>
                    {project.name}
                  </span>
                  <span className="text-xs text-muted-foreground group-hover:hidden">
                    {tasks.filter((t) => t.projectId === project.id && !t.parentId).length}
                  </span>
                </button>
                <div className="absolute right-1 top-1/2 -translate-y-1/2 flex items-center gap-0.5 opacity-0 group-hover:opacity-100 transition-all bg-card/80 backdrop-blur-sm rounded px-1">
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      updateProject(project.id, { isArchived: !project.isArchived });
                    }}
                    className="p-1.5 hover:bg-accent rounded text-muted-foreground hover:text-foreground"
                    title={project.isArchived ? "Restore project" : "Archive project"}
                  >
                    {project.isArchived ? <ArchiveRestore className="w-4 h-4" /> : <Archive className="w-4 h-4" />}
                  </button>
                  <button
                    onClick={(e) => {
                      e.stopPropagation();
                      if (confirm(`Delete project "${project.name}" and all its tasks?`)) {
                        deleteProject(project.id);
                        if (selectedProject === project.id) setSelectedProject("");
                      }
                    }}
                    className="p-1.5 hover:bg-destructive/10 rounded text-muted-foreground hover:text-destructive"
                    title="Delete project"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              </div>
            ))}
            
            <button
              onClick={() => setShowArchivedProjects(!showArchivedProjects)}
              className="w-full text-left px-3 py-1 text-[10px] uppercase tracking-wider text-muted-foreground hover:text-foreground transition-colors mt-4"
            >
              {showArchivedProjects ? "Hide Archived" : "Show Archived"}
            </button>
          </div>

          {showNewProject ? (
            <div className="mt-4">
              <input
                type="text"
                placeholder="Project name..."
                value={newProjectName}
                onChange={(e) => setNewProjectName(e.target.value)}
                onKeyDown={(e) => e.key === "Enter" && handleAddProject()}
                className="w-full px-3 py-2 bg-input-background rounded-lg border border-border mb-2"
                autoFocus
              />
              <div className="flex gap-2 mb-3 flex-wrap">
                {["#3b82f6", "#10b981", "#f59e0b", "#ef4444", "#ec4899", "#64748b"].map((c) => (
                  <button
                    key={c}
                    onClick={() => setNewProjectColor(c)}
                    className={`w-6 h-6 rounded-full border-2 transition-all ${
                      newProjectColor === c ? "border-foreground scale-110 shadow-sm" : "border-transparent opacity-70 hover:opacity-100"
                    }`}
                    style={{ backgroundColor: c }}
                  />
                ))}
              </div>
              <div className="flex gap-2">
                <button
                  onClick={handleAddProject}
                  className="flex-1 px-3 py-1 bg-primary text-primary-foreground rounded text-sm"
                >
                  Add
                </button>
                <button
                  onClick={() => {
                    setShowNewProject(false);
                    setNewProjectName("");
                  }}
                  className="flex-1 px-3 py-1 bg-secondary text-secondary-foreground rounded text-sm"
                >
                  Cancel
                </button>
              </div>
            </div>
          ) : (
            <button
              onClick={() => setShowNewProject(true)}
              className="w-full px-3 py-2 border border-dashed border-border rounded-lg hover:bg-accent/50 transition-colors flex items-center justify-center gap-2 text-muted-foreground"
            >
              <Plus className="w-4 h-4" />
              New Project
            </button>
          )}
        </div>

        {/* Tasks List */}
        <div className="flex-1 overflow-auto p-6">
          {/* New Task Input */}
          <div className="mb-6 bg-card border border-border rounded-lg p-4">
            <input
              id="new-task-input"
              type="text"
              placeholder="What needs to be done?"
              value={newTaskTitle}
              onChange={(e) => setNewTaskTitle(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter") handleAddTask();
              }}
              className="w-full bg-transparent border-none outline-none text-lg"
            />
            {newTaskTitle && (
              <div className="mt-3 flex flex-wrap gap-2">
                <select
                  value={selectedProject}
                  onChange={(e) => setSelectedProject(e.target.value)}
                  className="px-3 py-1 bg-secondary text-secondary-foreground rounded-lg text-sm"
                >
                  <option value="">No Project</option>
                  {projects.map((p) => (
                    <option key={p.id} value={p.id}>
                      {p.name}
                    </option>
                  ))}
                </select>
                <select
                  value={newTaskPriority}
                  onChange={(e) => setNewTaskPriority(parseInt(e.target.value))}
                  className="px-3 py-1 bg-secondary text-secondary-foreground rounded-lg text-sm"
                >
                  <option value={1}>High Priority</option>
                  <option value={2}>Medium Priority</option>
                  <option value={3}>Low Priority</option>
                  <option value={4}>No Priority</option>
                </select>
                <div className="relative">
                  <input
                    type="text"
                    placeholder="Due: tomorrow, monday…"
                    value={naturalDateInput}
                    onChange={(e) => setNaturalDateInput(e.target.value)}
                    className="px-3 py-1 bg-secondary text-secondary-foreground rounded-lg text-sm w-44"
                  />
                  {naturalDateInput && parseNaturalDate(naturalDateInput) && (
                    <span className="absolute right-2 top-1/2 -translate-y-1/2 text-[10px] text-primary">
                      {format(parseNaturalDate(naturalDateInput)!, "MMM d")}
                    </span>
                  )}
                </div>
                <button
                  onClick={() => handleAddTask()}
                  className="px-4 py-1 bg-primary text-primary-foreground rounded-lg text-sm"
                >
                  Add Task
                </button>
              </div>
            )}
          </div>

          {/* Tasks */}
          <div className="space-y-2">
            <AnimatePresence mode="popLayout">
              {sortedAndFilteredTasks.map((task) => (
                <motion.div
                  key={task.id}
                  layout
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  exit={{ opacity: 0, scale: 0.95 }}
                  transition={{ duration: 0.2 }}
                >
                  <TaskItem
                    task={task}
                    subtasks={getSubtasks(task.id)}
                    projects={projects}
                    expanded={expandedTasks.has(task.id)}
                    onToggle={() => handleToggleTask(task.id)}
                    onDelete={() => deleteTask(task.id)}
                    onToggleExpand={() => toggleExpanded(task.id)}
                    onUpdate={(updates) => updateTask(task.id, updates)}
                    onAddSubtask={(title) => {
                      addTask({
                        title,
                        completed: false,
                        tags: [],
                        parentId: task.id,
                        projectId: task.projectId,
                        priority: task.priority,
                        isRecurring: false,
                      });
                    }}
                    onAIBreakdown={async () => {
                      const subtasks = await breakdownTask({ title: task.title, description: task.description });
                      subtasks.forEach((st) =>
                        addTask({
                          title: st.title,
                          completed: false,
                          tags: [],
                          parentId: task.id,
                          projectId: task.projectId,
                          priority: st.priority ?? 2,
                          isRecurring: false,
                        })
                      );
                    }}
                    isOverdue={isOverdue(task)}
                    isSelected={selectedTaskIds.has(task.id)}
                    onSelect={() => toggleSelectTask(task.id)}
                    onStartTimer={() => navigate(`/timer?taskId=${task.id}`)}
                  />
                </motion.div>
              ))}
            </AnimatePresence>
            
            {sortedAndFilteredTasks.length === 0 && (
              <motion.div 
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="text-center py-24 text-muted-foreground bg-muted/5 rounded-2xl border border-dashed border-border mt-8"
              >
                <div className="bg-muted w-16 h-16 rounded-full flex items-center justify-center mx-auto mb-4">
                  <CheckSquare className="w-8 h-8 opacity-20" />
                </div>
                <h3 className="text-foreground text-lg mb-1">Clean slate!</h3>
                <p>No tasks found. Time to relax or start something new.</p>
                {searchQuery && (
                  <button 
                    onClick={() => setSearchQuery("")}
                    className="mt-4 text-primary text-sm hover:underline"
                  >
                    Clear search filters
                  </button>
                )}
              </motion.div>
            )}
          </div>
        </div>
      </div>

      {/* Bulk Action Toolbar */}
      {selectedTaskIds.size > 0 && (
        <div className="fixed bottom-8 left-1/2 -translate-x-1/2 bg-primary text-primary-foreground px-6 py-3 rounded-full shadow-2xl flex items-center gap-6 animate-in slide-in-from-bottom-4">
          <span className="font-medium">{selectedTaskIds.size} selected</span>
          <div className="w-px h-4 bg-primary-foreground/20" />
          <div className="flex gap-4">
            <button 
              onClick={handleBulkToggle}
              className="flex items-center gap-2 hover:opacity-80 transition-opacity"
            >
              <CheckSquare className="w-4 h-4" /> Toggle Status
            </button>
            <button 
              onClick={handleBulkDelete}
              className="flex items-center gap-2 hover:text-destructive-foreground transition-colors"
            >
              <Trash2 className="w-4 h-4" /> Delete
            </button>
          </div>
          <button 
            onClick={() => setSelectedTaskIds(new Set())}
            className="ml-2 p-1 hover:bg-primary-foreground/10 rounded-full transition-colors"
          >
            <Plus className="w-4 h-4 rotate-45" />
          </button>
        </div>
      )}
    </div>
  );
}

interface TaskItemProps {
  task: Task;
  subtasks: Task[];
  projects: any[];
  expanded: boolean;
  onToggle: () => void;
  onDelete: () => void;
  onToggleExpand: () => void;
  onUpdate: (updates: Partial<Task>) => void;
  onAddSubtask: (title: string) => void;
  onAIBreakdown: () => void;
  isOverdue: boolean;
  isSelected: boolean;
  onSelect: () => void;
  onStartTimer: () => void;
}

const PRIORITY_MAP: Record<number, { label: string; color: string; icon: any }> = {
  1: { label: "High", color: "text-red-500", icon: AlertCircle },
  2: { label: "Medium", color: "text-orange-500", icon: Flag },
  3: { label: "Low", color: "text-blue-500", icon: Flag },
  4: { label: "None", color: "text-muted-foreground", icon: Flag },
};

function TaskItem({
  task,
  subtasks,
  projects,
  expanded,
  onToggle,
  onDelete,
  onToggleExpand,
  onUpdate,
  onAddSubtask,
  onAIBreakdown,
  isOverdue,
  isSelected,
  onSelect,
  onStartTimer,
}: TaskItemProps) {
  const [aiBreaking, setAIBreaking] = useState(false);
  const [showSubtaskInput, setShowSubtaskInput] = useState(false);
  const [subtaskTitle, setSubtaskTitle] = useState("");
  const [isEditing, setIsEditing] = useState(false);
  const [editTitle, setEditTitle] = useState(task.title);
  const [showDetails, setShowDetails] = useState(false);

  const project = projects.find((p) => p.id === task.projectId);
  const hasSubtasks = subtasks.length > 0;

  const handleAddSubtask = () => {
    if (!subtaskTitle.trim()) return;
    onAddSubtask(subtaskTitle);
    setSubtaskTitle("");
    setShowSubtaskInput(false);
  };

  const handleSaveEdit = () => {
    if (editTitle.trim()) {
      onUpdate({ title: editTitle });
    }
    setIsEditing(false);
  };

  const priorityInfo = PRIORITY_MAP[task.priority] || PRIORITY_MAP[4];
  const PriorityIcon = priorityInfo.icon;

  return (
    <div className={`bg-card border rounded-lg overflow-hidden transition-all ${isSelected ? "border-primary ring-1 ring-primary" : "border-border"}`}>
      <div className="p-4 flex items-start gap-3 group hover:bg-accent/30 transition-colors">
        <input 
          type="checkbox"
          checked={isSelected}
          onChange={onSelect}
          className="mt-1.5 w-4 h-4 rounded border-muted-foreground bg-transparent cursor-pointer"
        />
        {hasSubtasks && (
          <button
            onClick={onToggleExpand}
            aria-label={expanded ? "Collapse subtasks" : "Expand subtasks"}
            className="mt-1 text-muted-foreground hover:text-foreground transition-colors"
          >
            {expanded ? (
              <ChevronDown className="w-4 h-4" />
            ) : (
              <ChevronRight className="w-4 h-4" />
            )}
          </button>
        )}
        {!hasSubtasks && <div className="w-4" />}

        <button
          onClick={onToggle}
          aria-label={task.completed ? "Mark task incomplete" : "Mark task complete"}
          className={`mt-1 w-6 h-6 rounded border-2 flex items-center justify-center transition-all flex-shrink-0 ${
            task.completed
              ? "bg-primary border-primary"
              : "border-muted-foreground hover:border-primary"
          }`}
        >
          {task.completed && <Check className="w-4 h-4 text-primary-foreground" />}
        </button>

        <div className="flex-1 min-w-0" onClick={() => !isEditing && setShowDetails(!showDetails)}>
          {isEditing ? (
            <input
              value={editTitle}
              onChange={(e) => setEditTitle(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter") handleSaveEdit();
                if (e.key === "Escape") {
                  setIsEditing(false);
                  setEditTitle(task.title);
                }
              }}
              onBlur={handleSaveEdit}
              className="w-full bg-input-background px-2 py-1 rounded border border-border"
              autoFocus
            />
          ) : (
            <div
              className={`cursor-pointer truncate ${task.completed ? "line-through text-muted-foreground" : ""}`}
              onClick={() => setIsEditing(true)}
              title={task.title}
            >
              {task.title}
            </div>
          )}

          <div className="flex items-center gap-3 mt-2 text-xs">
            <div className={`flex items-center gap-1 ${priorityInfo.color}`} title={`Priority: ${priorityInfo.label}`}>
              <PriorityIcon className="w-3 h-3" />
              <span>{priorityInfo.label}</span>
            </div>
            {project && (
              <div className="flex items-center gap-1.5">
                <div
                  className="w-3 h-3 rounded-full flex-shrink-0"
                  style={{ backgroundColor: project.color }}
                />
                <span className="text-muted-foreground truncate max-w-[120px]" title={project.name}>{project.name}</span>
              </div>
            )}
            {task.focusMinutes > 0 && (
              <div className="flex items-center gap-1.5 text-muted-foreground">
                <Clock className="w-3 h-3" />
                <span>{task.focusMinutes}m focused</span>
              </div>
            )}
            {task.dueDate && (
              <div
                className={`flex items-center gap-1.5 ${isOverdue ? "text-destructive" : "text-muted-foreground"}`}
              >
                <Calendar className="w-3 h-3" />
                <span>{format(task.dueDate, "MMM d")}</span>
              </div>
            )}
            {task.tags.length > 0 && (
              <div className="flex items-center gap-1.5 text-muted-foreground">
                <Tag className="w-3 h-3" />
                <span>{task.tags.join(", ")}</span>
              </div>
            )}
            {task.isRecurring && (
              <div className="flex items-center gap-1.5 text-primary">
                <RotateCw className="w-3 h-3" />
                <span>Recurring</span>
              </div>
            )}
          </div>
        </div>

        <div className="flex items-center gap-2 opacity-0 group-hover:opacity-100 transition-opacity">
          {!task.completed && (
            <button
              onClick={(e) => { e.stopPropagation(); onStartTimer(); }}
              className="p-1 hover:bg-primary/20 rounded text-primary transition-colors"
              title="Start Focus Timer"
              aria-label="Start Focus Timer"
            >
              <Play className="w-4 h-4 fill-current" />
            </button>
          )}
          {!task.completed && (
            <button
              onClick={async (e) => {
                e.stopPropagation();
                setAIBreaking(true);
                await onAIBreakdown();
                setAIBreaking(false);
              }}
              disabled={aiBreaking}
              className="p-1 hover:bg-blue-500/20 rounded text-blue-400 transition-colors disabled:opacity-50"
              title="AI: Break into subtasks"
              aria-label="AI breakdown"
            >
              {aiBreaking ? (
                <Loader2 className="w-4 h-4 animate-spin" />
              ) : (
                <Sparkles className="w-4 h-4" />
              )}
            </button>
          )}
          <button
            onClick={() => setShowSubtaskInput(true)}
            className="p-1 hover:bg-accent rounded text-muted-foreground hover:text-foreground transition-colors"
            title="Add subtask"
            aria-label="Add subtask"
          >
            <Plus className="w-4 h-4" />
          </button>
          <button
            onClick={onDelete}
            className="p-1 hover:bg-destructive/10 rounded text-muted-foreground hover:text-destructive transition-colors"
            title="Delete task"
            aria-label="Delete task"
          >
            <Trash2 className="w-4 h-4" />
          </button>
        </div>
      </div>

      {showDetails && (
        <div className="px-14 pb-4 space-y-4 bg-muted/10 border-t border-border/50 pt-4">
          <div className="grid grid-cols-2 gap-4">
            <div>
              <label className="block text-xs font-medium text-muted-foreground mb-1 flex items-center gap-1">
                <Flag className="w-3 h-3" /> Priority
              </label>
              <select
                value={task.priority}
                onChange={(e) => onUpdate({ priority: parseInt(e.target.value) })}
                className="w-full bg-input-background px-2 py-1 rounded border border-border text-sm"
              >
                <option value={1}>High</option>
                <option value={2}>Medium</option>
                <option value={3}>Low</option>
                <option value={4}>None</option>
              </select>
            </div>
            <div>
              <label className="block text-xs font-medium text-muted-foreground mb-1 flex items-center gap-1">
                <Calendar className="w-3 h-3" /> Due Date
              </label>
              <input
                type="date"
                value={task.dueDate ? new Date(task.dueDate).toISOString().split("T")[0] : ""}
                onChange={(e) => onUpdate({ dueDate: e.target.value ? new Date(e.target.value) : undefined })}
                className="w-full bg-input-background px-2 py-1 rounded border border-border text-sm"
              />
            </div>
          </div>

          <div>
            <label className="block text-xs font-medium text-muted-foreground mb-1 flex items-center gap-1">
              <FileText className="w-3 h-3" /> Description
            </label>
            <textarea
              value={task.description || ""}
              onChange={(e) => onUpdate({ description: e.target.value })}
              placeholder="Add a description..."
              className="w-full bg-input-background px-2 py-1 rounded border border-border text-sm min-h-[60px] resize-none"
            />
          </div>

          <div>
            <label className="block text-xs font-medium text-muted-foreground mb-1 flex items-center gap-1">
              <FileText className="w-3 h-3" /> Notes
            </label>
            <textarea
              value={task.notes || ""}
              onChange={(e) => onUpdate({ notes: e.target.value })}
              placeholder="Add personal notes..."
              className="w-full bg-input-background px-2 py-1 rounded border border-border text-sm min-h-[60px] resize-none"
            />
          </div>

          <div>
            <label className="block text-xs font-medium text-muted-foreground mb-1 flex items-center gap-1">
              <Tag className="w-3 h-3" /> Tags
            </label>
            <div className="flex flex-wrap gap-2 mb-2">
              {task.tags.map((tag) => (
                <span key={tag} className="px-2 py-0.5 bg-primary/10 text-primary rounded-full text-xs flex items-center gap-1">
                  {tag}
                  <button 
                    onClick={() => onUpdate({ tags: task.tags.filter(t => t !== tag) })}
                    className="hover:text-foreground"
                  >
                    ×
                  </button>
                </span>
              ))}
            </div>
            <input
              type="text"
              placeholder="Add tag (press Enter)..."
              onKeyDown={(e) => {
                if (e.key === "Enter") {
                  const val = e.currentTarget.value.trim();
                  if (val && !task.tags.includes(val)) {
                    onUpdate({ tags: [...task.tags, val] });
                    e.currentTarget.value = "";
                  }
                }
              }}
              className="w-full bg-input-background px-2 py-1 rounded border border-border text-sm"
            />
          </div>

          <div className="flex items-center gap-2 pt-2">
            <button
              onClick={() => onUpdate({ isRecurring: !task.isRecurring })}
              className={`flex items-center gap-2 px-3 py-1 rounded text-xs transition-colors ${
                task.isRecurring ? "bg-primary/20 text-primary border border-primary/30" : "bg-muted text-muted-foreground hover:bg-muted/80"
              }`}
            >
              <RotateCw className="w-3 h-3" />
              {task.isRecurring ? "Recurring Enabled" : "Make Recurring"}
            </button>
          </div>
        </div>
      )}

      {expanded && hasSubtasks && (
        <div className="pl-10 pr-4 pb-4 space-y-2 bg-muted/20">
          {subtasks.map((subtask) => (
            <div
              key={subtask.id}
              className="flex items-center gap-3 p-2 rounded hover:bg-accent/30 transition-colors group"
            >
              <button
                onClick={() => onUpdate({ completed: !subtask.completed })}
                aria-label={subtask.completed ? "Mark subtask incomplete" : "Mark subtask complete"}
                className={`w-5 h-5 rounded border-2 flex items-center justify-center transition-all flex-shrink-0 ${
                  subtask.completed
                    ? "bg-primary border-primary"
                    : "border-muted-foreground hover:border-primary"
                }`}
              >
                {subtask.completed && <Check className="w-3 h-3 text-primary-foreground" />}
              </button>
              <span
                className={`flex-1 text-sm truncate ${subtask.completed ? "line-through text-muted-foreground" : ""}`}
                title={subtask.title}
              >
                {subtask.title}
              </span>
              <button
                onClick={() => onDelete()}
                aria-label="Delete subtask"
                className="opacity-0 group-hover:opacity-100 p-1 hover:bg-destructive/10 rounded text-muted-foreground hover:text-destructive transition-all"
              >
                <Trash2 className="w-3 h-3" />
              </button>
            </div>
          ))}
        </div>
      )}

      {showSubtaskInput && (
        <div className="pl-10 pr-4 pb-4 bg-muted/20">
          <input
            type="text"
            placeholder="Subtask title..."
            value={subtaskTitle}
            onChange={(e) => setSubtaskTitle(e.target.value)}
            onKeyDown={(e) => {
              if (e.key === "Enter") handleAddSubtask();
              if (e.key === "Escape") {
                setShowSubtaskInput(false);
                setSubtaskTitle("");
              }
            }}
            className="w-full px-3 py-2 bg-input-background rounded-lg border border-border text-sm"
            autoFocus
          />
        </div>
      )}
    </div>
  );
}
