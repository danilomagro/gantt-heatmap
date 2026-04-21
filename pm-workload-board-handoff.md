# PM Workload Board — Handoff Prompt for Claude

## Context

This file is a prompt to give to Claude (or another AI) to continue development
of the attached `pm-workload-board.html` tool.

---

## What this tool is

A **standalone** web application (single HTML file, no server, no installation)
for visualizing the workload of a development team across multiple parallel projects.

**Problem it solves:** a PM manages 7–8 maintenance projects + heavy implementations
(lasting 1–2+ weeks). When management asks why developers are slow,
you need an **objective and unassailable** visual artifact that shows real overlaps.

---

## Technical architecture

- **Stack:** HTML + React 18 (via CDN) + Babel standalone (compiles JSX in the browser)
- **Storage:** browser `localStorage` — data persists across sessions
- **Zero local dependencies:** works offline after the first load, double-click to open
- **Export/Import JSON:** to sync data across different devices

---

## Data structure (localStorage, key `pm-gantt-v2`)

```json
{
  "t": [
    {
      "id": "timestamp string",
      "taskName": "Activity name",
      "projectName": "Project name",
      "resourceId": "resource id",
      "startDate": "YYYY-MM-DD",
      "endDate": "YYYY-MM-DD"
    }
  ],
  "r": [
    { "id": "timestamp string", "name": "Resource name" }
  ],
  "c": {
    "Project name": "#HEX color assigned automatically"
  }
}
```

---

## Current features

**Left sidebar:**
- Resource (people) management: add / delete
- Project legend with auto-assigned colors
- Add/edit task form (task name, project, resource, start/end dates)
- Task list with edit and delete
- Export JSON / Import JSON buttons

**Main area:**
- Toggle between three views: Gantt / Heatmap / Both
- **Gantt:** cross-project timeline, grouped by resource, color-coded bars by project,
  red line = today, colored badge on resource name (blue/yellow/red based on task count),
  click a bar = edit
- **Heatmap:** resource × week grid, number of parallel activities per cell,
  colors from blue (1) → yellow (2) → orange (3) → red (4+), hover = tooltip with details

**Timeline:** automatically calculated from task dates (with a minimum padding of 8 weeks).

---

## Relevant design decisions

- Project colors are automatically assigned from a fixed 10-color palette
  (`COLORS` array), without user intervention
- The heatmap is **derived** from the Gantt, not filled in manually — this is the key point
  for credibility with management ("the red isn't my decision, the bars decide it")
- Dark theme: background `#0A0F1E`, sidebar `#111827`
- Font: Segoe UI / system-ui (no CDN fonts, to work offline)

---

## Possible future development steps

Listed in suggested priority order:

1. **Resource filter** — show only a selected resource in the Gantt view
2. **Task notes** — free text field, visible in the bar hover tooltip
3. **Multi-resource per task** — assign multiple resources to the same task (currently 1:1)
4. **Horizontal scroll / timeline navigation** — scroll left/right to navigate the timeline
   when tasks span many weeks, keeping bar proportions fixed
5. **Print / PDF export** — "Print" button optimized for the browser print dialog
   (print CSS, dark background preserved, sidebar hidden)
6. **Milestone** — vertical marker with label (e.g. "Project X go-live") overlaid on the Gantt
7. **Drag & drop dates** — drag bars to shift dates (high complexity)
8. **Completion percentage** — partial fill bar + % field in the task card
9. **Light theme** — light colour scheme alternative to the current dark theme, with a toggle button (top-right) and preference saved in localStorage

---

## How to use this prompt

1. Attach this `.md` file + the `pm-workload-board.html` file to Claude
2. Write: *"Read the handoff file and the attached HTML code, then implement [feature X]"*
3. Claude will return the updated HTML file to replace the previous one

**Note:** the HTML file is self-contained, so every change produces a complete new file
to be replaced entirely — no partial patches.
