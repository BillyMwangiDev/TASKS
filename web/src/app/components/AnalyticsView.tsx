import { useMemo } from "react";
import { useTaskyData } from "../hooks/useTaskyData";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  LineChart,
  Line,
  Area,
  AreaChart,
} from "recharts";
import {
  startOfDay,
  endOfDay,
  eachDayOfInterval,
  subDays,
  format,
  startOfHour,
  getHours,
  isToday,
  isSameDay,
} from "date-fns";
import { TrendingUp, Clock, Target, Flame } from "lucide-react";

export function AnalyticsView() {
  const { tasks, focusSessions } = useTaskyData();

  // Calculate stats
  const stats = useMemo(() => {
    const today = new Date();
    const todayStart = startOfDay(today);
    const todayEnd = endOfDay(today);

    const todayTasks = tasks.filter(
      (t) => t.completedAt && t.completedAt >= todayStart && t.completedAt <= todayEnd
    );

    const todaySessions = focusSessions.filter(
      (s) => s.completed && s.startTime >= todayStart && s.startTime <= todayEnd
    );

    const totalFocusMinutes = Math.round(
      todaySessions.reduce((sum, s) => sum + s.duration, 0) / 60
    );

    const completionRate =
      tasks.length > 0 ? Math.round((tasks.filter((t) => t.completed).length / tasks.length) * 100) : 0;

    const currentStreak = calculateStreak(tasks);

    return {
      tasksCompletedToday: todayTasks.length,
      focusMinutesToday: totalFocusMinutes,
      completionRate,
      currentStreak,
    };
  }, [tasks, focusSessions]);

  // Daily completion data (last 30 days)
  const dailyData = useMemo(() => {
    const days = eachDayOfInterval({
      start: subDays(new Date(), 29),
      end: new Date(),
    });

    return days.map((day, index) => {
      const dayStart = startOfDay(day);
      const dayEnd = endOfDay(day);

      const completed = tasks.filter(
        (t) => t.completedAt && t.completedAt >= dayStart && t.completedAt <= dayEnd
      ).length;

      const focusMinutes = Math.round(
        focusSessions
          .filter((s) => s.completed && s.startTime >= dayStart && s.startTime <= dayEnd)
          .reduce((sum, s) => sum + s.duration, 0) / 60
      );

      return {
        date: format(day, "MMM d"),
        dateKey: format(day, "yyyy-MM-dd"),
        completed,
        focusMinutes,
      };
    });
  }, [tasks, focusSessions]);

  // Hourly breakdown
  const hourlyData = useMemo(() => {
    const hours = Array.from({ length: 24 }, (_, i) => i);

    return hours.map((hour) => {
      const sessions = focusSessions.filter((s) => {
        const sessionHour = getHours(s.startTime);
        return sessionHour === hour && s.completed;
      });

      const focusMinutes = Math.round(sessions.reduce((sum, s) => sum + s.duration, 0) / 60);

      return {
        hour: format(new Date().setHours(hour, 0, 0, 0), "ha"),
        hourValue: hour,
        focusMinutes,
      };
    });
  }, [focusSessions]);

  // Focus heatmap (last 90 days)
  const heatmapData = useMemo(() => {
    const days = eachDayOfInterval({
      start: subDays(new Date(), 89),
      end: new Date(),
    });

    const data = days.map((day) => {
      const dayStart = startOfDay(day);
      const dayEnd = endOfDay(day);

      const focusMinutes = Math.round(
        focusSessions
          .filter((s) => s.completed && s.startTime >= dayStart && s.startTime <= dayEnd)
          .reduce((sum, s) => sum + s.duration, 0) / 60
      );

      return {
        date: day,
        value: focusMinutes,
      };
    });

    // Group by week
    const weeks: { date: string; days: typeof data }[] = [];
    let currentWeek: typeof data = [];

    data.forEach((day, index) => {
      currentWeek.push(day);
      if (currentWeek.length === 7 || index === data.length - 1) {
        weeks.push({
          date: format(currentWeek[0].date, "MMM d"),
          days: [...currentWeek],
        });
        currentWeek = [];
      }
    });

    return weeks;
  }, [focusSessions]);

  const maxHeatmapValue = Math.max(...heatmapData.flatMap((w) => w.days.map((d) => d.value)), 1);

  return (
    <div className="h-full overflow-auto p-8 bg-gradient-to-br from-background to-muted/20">
      <div className="max-w-7xl mx-auto">
        <h2 className="mb-8">Productivity Analytics</h2>

        {/* Stats Grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <StatCard
            icon={Target}
            label="Tasks Today"
            value={stats.tasksCompletedToday}
            color="text-blue-500"
          />
          <StatCard
            icon={Clock}
            label="Focus Minutes"
            value={stats.focusMinutesToday}
            suffix="m"
            color="text-blue-500"
          />
          <StatCard
            icon={TrendingUp}
            label="Completion Rate"
            value={stats.completionRate}
            suffix="%"
            color="text-green-500"
          />
          <StatCard
            icon={Flame}
            label="Current Streak"
            value={stats.currentStreak}
            suffix=" days"
            color="text-orange-500"
          />
        </div>

        {/* Charts Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          {/* Daily Completion */}
          <div className="bg-card border border-border rounded-lg p-6">
            <h3 className="mb-4">Daily Completion (Last 30 Days)</h3>
            <ResponsiveContainer width="100%" height={250}>
              <AreaChart data={dailyData}>
                <defs>
                  <linearGradient id="colorCompleted" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="rgb(59, 130, 246)" stopOpacity={0.3} />
                    <stop offset="95%" stopColor="rgb(59, 130, 246)" stopOpacity={0} />
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                <XAxis
                  dataKey="date"
                  stroke="rgba(255,255,255,0.5)"
                  tick={{ fontSize: 12 }}
                />
                <YAxis stroke="rgba(255,255,255,0.5)" tick={{ fontSize: 12 }} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: "rgba(0,0,0,0.9)",
                    border: "1px solid rgba(255,255,255,0.1)",
                    borderRadius: "8px",
                  }}
                />
                <Area
                  type="monotone"
                  dataKey="completed"
                  stroke="rgb(59, 130, 246)"
                  strokeWidth={2}
                  fill="url(#colorCompleted)"
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>

          {/* Daily Focus Minutes */}
          <div className="bg-card border border-border rounded-lg p-6">
            <h3 className="mb-4">Focus Minutes (Last 30 Days)</h3>
            <ResponsiveContainer width="100%" height={250}>
              <BarChart data={dailyData}>
                <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
                <XAxis
                  dataKey="date"
                  stroke="rgba(255,255,255,0.5)"
                  tick={{ fontSize: 12 }}
                />
                <YAxis stroke="rgba(255,255,255,0.5)" tick={{ fontSize: 12 }} />
                <Tooltip
                  contentStyle={{
                    backgroundColor: "rgba(0,0,0,0.9)",
                    border: "1px solid rgba(255,255,255,0.1)",
                    borderRadius: "8px",
                  }}
                />
                <Bar dataKey="focusMinutes" fill="rgb(59, 130, 246)" radius={[8, 8, 0, 0]} />
              </BarChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Hourly Breakdown */}
        <div className="bg-card border border-border rounded-lg p-6 mb-8">
          <h3 className="mb-4">Hourly Focus Distribution</h3>
          <ResponsiveContainer width="100%" height={250}>
            <LineChart data={hourlyData}>
              <CartesianGrid strokeDasharray="3 3" stroke="rgba(255,255,255,0.1)" />
              <XAxis dataKey="hour" stroke="rgba(255,255,255,0.5)" tick={{ fontSize: 12 }} />
              <YAxis stroke="rgba(255,255,255,0.5)" tick={{ fontSize: 12 }} />
              <Tooltip
                contentStyle={{
                  backgroundColor: "rgba(0,0,0,0.9)",
                  border: "1px solid rgba(255,255,255,0.1)",
                  borderRadius: "8px",
                }}
              />
              <Line
                type="monotone"
                dataKey="focusMinutes"
                stroke="rgb(16, 185, 129)"
                strokeWidth={3}
                dot={{ fill: "rgb(16, 185, 129)", r: 4 }}
              />
            </LineChart>
          </ResponsiveContainer>
          <p className="text-sm text-muted-foreground mt-4 text-center">
            Identify your peak productivity hours to optimize your schedule
          </p>
        </div>

        {/* Focus Heatmap */}
        <div className="bg-card border border-border rounded-lg p-6">
          <h3 className="mb-4">Focus Activity Heatmap (Last 90 Days)</h3>
          <div className="overflow-x-auto">
            <div className="inline-flex flex-col gap-1 min-w-full">
              {["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"].map((day, dayIndex) => (
                <div key={day} className="flex items-center gap-1">
                  <div className="w-8 text-xs text-muted-foreground">{day}</div>
                  <div className="flex gap-1">
                    {heatmapData.map((week, weekIndex) => {
                      const dayData = week.days[dayIndex];
                      if (!dayData) return <div key={weekIndex} className="w-3 h-3" />;

                      const intensity = dayData.value / maxHeatmapValue;
                      const isCurrentDay = isToday(dayData.date);

                      return (
                        <div
                          key={weekIndex}
                          className={`w-3 h-3 rounded-sm transition-all hover:ring-2 hover:ring-primary ${
                            isCurrentDay ? "ring-2 ring-primary" : ""
                          }`}
                          style={{
                            backgroundColor:
                              intensity === 0
                                ? "rgba(255,255,255,0.05)"
                                : `rgba(59, 130, 246, ${0.2 + intensity * 0.8})`,
                          }}
                          title={`${format(dayData.date, "MMM d, yyyy")}: ${dayData.value} minutes`}
                        />
                      );
                    })}
                  </div>
                </div>
              ))}
            </div>
          </div>
          <div className="flex items-center justify-between mt-6">
            <p className="text-sm text-muted-foreground">Less</p>
            <div className="flex gap-1">
              {[0, 0.25, 0.5, 0.75, 1].map((intensity) => (
                <div
                  key={intensity}
                  className="w-4 h-4 rounded-sm"
                  style={{
                    backgroundColor:
                      intensity === 0
                        ? "rgba(255,255,255,0.05)"
                        : `rgba(59, 130, 246, ${0.2 + intensity * 0.8})`,
                  }}
                />
              ))}
            </div>
            <p className="text-sm text-muted-foreground">More</p>
          </div>
        </div>
      </div>
    </div>
  );
}

interface StatCardProps {
  icon: React.ElementType;
  label: string;
  value: number;
  suffix?: string;
  color: string;
}

function StatCard({ icon: Icon, label, value, suffix = "", color }: StatCardProps) {
  return (
    <div className="bg-card border border-border rounded-lg p-6">
      <div className="flex items-start justify-between mb-3">
        <div className={`p-2 rounded-lg bg-muted ${color}`}>
          <Icon className="w-5 h-5" />
        </div>
      </div>
      <div className="text-3xl mb-1">
        {value}
        {suffix}
      </div>
      <div className="text-sm text-muted-foreground">{label}</div>
    </div>
  );
}

function calculateStreak(tasks: any[]): number {
  const completedByDay = new Map<string, number>();

  tasks.forEach((task) => {
    if (task.completedAt) {
      const dateKey = format(startOfDay(task.completedAt), "yyyy-MM-dd");
      completedByDay.set(dateKey, (completedByDay.get(dateKey) || 0) + 1);
    }
  });

  let streak = 0;
  let currentDate = new Date();

  while (true) {
    const dateKey = format(startOfDay(currentDate), "yyyy-MM-dd");
    if (completedByDay.has(dateKey)) {
      streak++;
      currentDate = subDays(currentDate, 1);
    } else {
      break;
    }
  }

  return streak;
}