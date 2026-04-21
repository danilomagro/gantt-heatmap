# ◈ PM WORKLOAD BOARD

> *"If the team looks slow, show them the bars. If they still don't believe you, show them the heatmap."*

A single-file **cross-project Gantt and capacity heatmap tool** for project managers handling multiple simultaneous implementations. No backend, no dependencies to install, no build step. Just open `pm-workload-board.html`.

![PM Workload Board preview](preview.png)

---

## The problem it solves

Managing 5+ parallel implementations across a team? When management asks why delivery is slow, gut feeling doesn't cut it. This tool gives you an **objective, inattackable visual** — a Gantt that shows what's running and when, and a heatmap that derives team load automatically from the same data.

The heatmap is never filled in manually. Red means red because the bars say so.

---

## Features

| | |
|---|---|
| **Cross-project Gantt** | Timeline grouped by resource, bars coloured by project, red line = today, click bar to edit |
| **Capacity Heatmap** | Derived automatically from Gantt — resource × week grid, blue → amber → red by parallel task count |
| **Resource & Project filters** | Focus either view on one person or one project — filters compose, heatmap always shows real total load |
| **Multi-resource tasks** | Assign a task to multiple people — load propagates to each resource in both views |
| **Task notes** | Optional free-text notes per task, visible on hover, with a subtle dot indicator on the bar |
| **Export / Import JSON** | Full data portability — sync between devices or share snapshots with your team |
| **Synchronized horizontal scroll** | Both views scroll in sync when tasks span many weeks; resource column stays fixed |

---

## Usage

```bash
git clone https://github.com/danilomagro/gantt-heatmap.git
cd gantt-heatmap
```

Open `pm-workload-board.html` in your browser — no server needed, works offline after first load.

**To try it immediately**: click **Import** and select `sample-data.json` — a realistic 18-week scenario across 3 resources and 5 projects loads instantly.

---

## Technical notes

- Single HTML file — React 18 + Babel standalone loaded from CDN, everything else self-contained
- Data stored in `localStorage` — survives page reloads, no account required
- Nothing leaves your machine

---

## The making of

Most tools like this don't exist as single HTML files you can double-click. They're SaaS products, Jira plugins, or Excel macros that require setup, licenses, or IT approval.

This one started as a real need — a PM who wanted something lightweight, portable, and credible enough to show to management. No setup, no explanations required.

The implementation was handled entirely by **[Claude Code](https://claude.ai)** (Anthropic) through an iterative session. No code was written by hand — every feature was specified, refined, and corrected through natural language.

> **[Danilo Magro](https://www.linkedin.com/in/danilo-magro/)**'s role: the problem, the vision, the UX decisions, and the relentless "yes but what if..."  
> Claude's role: everything that runs in the browser.

---

## Status

🚧 **Work in progress** — actively developed.

- [ ] Print / PDF export
- [ ] Milestone markers on Gantt
- [ ] Drag & drop to reschedule tasks
- [ ] Completion percentage per task
- [ ] Light theme toggle

---

## License

MIT — do whatever you want with it.  
If you're a PM drowning in parallel projects, I hope this helps.
