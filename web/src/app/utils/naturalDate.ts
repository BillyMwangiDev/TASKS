/**
 * Parse natural language date expressions into Date objects.
 * Handles: today, tomorrow, yesterday, next week, end of month,
 *          day names (monday, tuesday...), relative (+Nd).
 */
export function parseNaturalDate(input: string): Date | null {
  const s = input.trim().toLowerCase();
  const today = new Date();
  today.setHours(23, 59, 0, 0);

  if (s === "today") return today;

  if (s === "tomorrow") {
    const d = new Date(today);
    d.setDate(d.getDate() + 1);
    return d;
  }

  if (s === "yesterday") {
    const d = new Date(today);
    d.setDate(d.getDate() - 1);
    return d;
  }

  if (s === "next week") {
    const d = new Date(today);
    d.setDate(d.getDate() + 7);
    return d;
  }

  if (s === "end of month" || s === "eom") {
    const d = new Date(today.getFullYear(), today.getMonth() + 1, 0);
    d.setHours(23, 59, 0, 0);
    return d;
  }

  if (s === "end of year" || s === "eoy") {
    return new Date(today.getFullYear(), 11, 31, 23, 59);
  }

  // Day names: "monday", "next monday"
  const days = ["sunday", "monday", "tuesday", "wednesday", "thursday", "friday", "saturday"];
  const dayMatch = days.findIndex((d) => s === d || s === `next ${d}`);
  if (dayMatch !== -1) {
    const d = new Date(today);
    const diff = (dayMatch - d.getDay() + 7) % 7 || 7;
    d.setDate(d.getDate() + diff);
    return d;
  }

  // "+Nd" shorthand: "+3d" = 3 days from now
  const relMatch = s.match(/^\+(\d+)d$/);
  if (relMatch) {
    const d = new Date(today);
    d.setDate(d.getDate() + parseInt(relMatch[1]));
    return d;
  }

  // Fallback: try native Date parse
  const native = new Date(input);
  if (!isNaN(native.getTime())) return native;

  return null;
}

/** Returns true if input looks like a natural date expression. */
export function isNaturalDate(input: string): boolean {
  return parseNaturalDate(input) !== null;
}
