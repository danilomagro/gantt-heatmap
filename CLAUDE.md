# PM Workload Board — project context for Claude

Single-file cross-project **Gantt + capacity heatmap** for PMs managing many parallel implementations.
Live: https://danilomagro.github.io/gantt-heatmap/pm-workload-board.html (GitHub Pages, deploys from `master`).

The owner (Danilo, a PM) drives product and UX decisions; Claude writes all the code. Talk to Danilo in Italian; code, comments, commits and README stay in English.

## Core design principle

The heatmap is **derived** from the Gantt, never filled in manually — "the red isn't my decision, the bars decide it." This is what makes the tool credible with management. Never add features that let users edit heatmap values directly.

## Architecture

- **`pm-workload-board.html` is the whole app**: React 18 + Babel standalone from cdnjs, JSX compiled in the browser. No build step, no npm, no backend. Keep it that way — no bundlers, no extra files the app depends on.
- `index.html` only redirects to the app and carries Open Graph tags. Don't rename or move either file: their URLs are shared publicly.
- Styling: inline style objects plus CSS custom properties (`--bg`, `--surface`, `--text-dim`, …) defined for `[data-theme="dark"]` and `[data-theme="light"]`. Use the variables, never hard-coded theme colours. Font: Segoe UI / system-ui (no web fonts, must work offline).
- Layout: the app is exactly `100vh`; `<main>` and the sidebar are the scroll containers (sticky headers depend on it — don't go back to `minHeight`). Section titles stick at top 0, week headers at the measured title height (`useMeasuredHeight`); `.pm-sticky` is reset to static in print. Sidebar sections never get their own scroller (an inner `flex:1` scroller collapses to 0px in the fixed-height column) — the whole sidebar scrolls.
- Overview (`density === "overview"`): one compact row per group (`renderGanttRow(row, true)`, lanes of `LANE_C` px, no text, move-only drag) and `dayW` fitted so `fitWeeks` fill the width; `colGran` picks week/month headers. Draw with `colGran`, never `granularity`, outside the toolbar.
- Positioning is driven by `dayW` (px per calendar day: Day 38, Week 80/7, Month 120/30.44). `LABEL_W` is the fixed label column shared by Gantt and heatmap.

## Data (localStorage)

Board data under key `pm-gantt-v2`:

```js
{
  t: [{ id, taskName, projectName, resourceIds: [id], startDate: "YYYY-MM-DD", endDate: "YYYY-MM-DD", notes, completion /* 0-100 or null */, allocation /* effort 1-100, missing = 100 */, tentative /* bool */ }],
  r: [{ id, name }],
  c: { "Project name": "#HEX" },          // auto-assigned from COLORS palette
  m: [{ id, name, date: "YYYY-MM-DD", color }],
  o: [{ id, resourceId, startDate, endDate, label }]   // time off
}
```

- `persist(t, r, c, m, o)` — `o` defaults to `timeOffRef.current`; pass it explicitly when the same handler changes time off. Nothing is written while previewing a shared board (`sharedRef`).
- `normalizeTasks()` migrates legacy `resourceId` (singular) → `resourceIds[]`. Keep backward compatibility with old exports and share links.
- UI preferences have their own keys: `pm-gantt-theme`, `pm-gantt-gran`, `pm-gantt-group`, `pm-gantt-tentative`, `pm-gantt-density`, `pm-gantt-moreOpen`, `pm-gantt-offOpen`, `pm-gantt-resOpen`, `pm-gantt-projOpen`, `pm-gantt-msOpen`, `pm-gantt-tasksOpen`. Wrap every localStorage access in try/catch.
- Heatmap load = Σ(effort × task working days the person is present) / days available (Mon–Fri minus time off), in %. A week fully off shows OFF; a task with effort ≥ `LIGHT_BELOW` on a day off is a ⚠ clash. `LOAD_STEPS` [100,200,300] map load to heat levels 1–4 (an all-100 % board reproduces the old parallel-task scale).
- Tentative tasks: `pm-gantt-tentative` = hide | show (default: visible, excluded from load, cell outlined) | count (included).
- Keep task creation light: only name, project, people, dates are visible; optional fields live under "More options" and new tasks inherit effort from the project's latest task.
- Share links encode the board as base64url JSON in `#board=…`; the app then shows a non-saving preview with "Import to my board".

- Sample data: `SAMPLE_DATA` is authored on a fixed calendar (anchor Mon 2026-04-20, scenario "today" = week 7). `buildSampleData()` shifts everything by whole weeks so that week lands on the real current week; keep notes and labels free of absolute dates or seasons. Completion values assume the scenario's today.

## Bar visual language

Solid bar = committed work; light tinted slimmer bar (`LIGHT_BELOW` 50 %) = background duty; diagonal stripes + dashed outline = tentative; grey hatch over the timeline = time off; thin dashed line under the bars = milestone (today is the only solid red line). Keep new states distinguishable from these.

## Typography

Target is a 1920×1080 office monitor at 100% Windows scaling. Minimum text 11px (10px only for day-view column headers); primary labels 12–13px; no 700/800 weights below 12px.

## Workflow

- Commit and push directly to `master` — **one self-contained commit per improvement** so it can be reverted easily. Keep the branch named `master`.
- Working tree uses **CRLF**; preserve it (`sed -i` strips CR — rewrite with Python `newline='\r\n'`).
- Verify visually before committing: serve with `python -m http.server 8765` and screenshot with headless Chrome at `--window-size=1920,1080 --force-device-scale-factor=1`, dark and light, Day/Week/Month. Use fresh `--user-data-dir` profiles, or Chrome serves a cached page.
- Keep README in sync when shipping a feature: features table, "Recently shipped", backlog. Regenerate `preview.png` when the UI changes visibly.
