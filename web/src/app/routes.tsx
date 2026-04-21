import { createHashRouter } from "react-router";
import { Layout } from "./components/Layout";
import { TasksView } from "./components/TasksView";
import { TimerView } from "./components/TimerView";
import { AnalyticsView } from "./components/AnalyticsView";

export const router = createHashRouter([
  {
    path: "/",
    Component: Layout,
    children: [
      { index: true, Component: TasksView },
      { path: "timer", Component: TimerView },
      { path: "analytics", Component: AnalyticsView },
    ],
  },
]);
