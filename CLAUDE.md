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
- Positioning is driven by `dayW` (px per calendar day: Day 38, Week 80/7, Month 120/30.44). `LABEL_W` is the fixed label column shared by Gantt and heatmap.

## Data (localStorage)

Board data under key `pm-gantt-v2`:

```js
{
  t: [{ id, taskName, projectName, resourceIds: [id], startDate: "YYYY-MM-DD", endDate: "YYYY-MM-DD", notes, completion /* 0-100 or "" */ }],
  r: [{ id, name }],
  c: { "Project name": "#HEX" },          // auto-assigned from COLORS palette
  m: [{ id, name, date: "YYYY-MM-DD", color }]
}
```

- `normalizeTasks()` migrates legacy `resourceId` (singular) → `resourceIds[]`. Keep backward compatibility with old exports and share links.
- UI preferences have their own keys: `pm-gantt-theme`, `pm-gantt-gran`, `pm-gantt-group`, `pm-gantt-resOpen`, `pm-gantt-msOpen`, `pm-gantt-tasksOpen`. Wrap every localStorage access in try/catch.
- Share links encode the board as base64url JSON in `#board=…`; the app then shows a non-saving preview with "Import to my board".

## Typography

Target is a 1920×1080 office monitor at 100% Windows scaling. Minimum text 11px (10px only for day-view column headers); primary labels 12–13px; no 700/800 weights below 12px.

## Workflow

- Commit and push directly to `master` — **one self-contained commit per improvement** so it can be reverted easily. Keep the branch named `master`.
- Working tree uses **CRLF**; preserve it (`sed -i` strips CR — rewrite with Python `newline='\r\n'`).
- Verify visually before committing: serve with `python -m http.server 8765` and screenshot with headless Chrome at `--window-size=1920,1080 --force-device-scale-factor=1`, dark and light, Day/Week/Month. Use fresh `--user-data-dir` profiles, or Chrome serves a cached page.
- Keep README in sync when shipping a feature: features table, "Recently shipped", backlog. Regenerate `preview.png` when the UI changes visibly.
