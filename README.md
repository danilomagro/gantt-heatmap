# gantt-heatmap

A cross-project Gantt + capacity heatmap tool for project managers handling multiple simultaneous implementations.

![Preview](preview.png)

---

## What it does

Project managers juggling 7–8 concurrent projects — a mix of maintenance and large implementations spanning weeks — need an objective, visual artifact to show management where team capacity is actually going.

**gantt-heatmap** solves this with two linked views:

- **Gantt** — inter-project timeline grouped by resource, color-coded by project, with a live "today" marker
- **Heatmap** — resource × week grid showing parallel workload intensity, derived automatically from the Gantt data (blue → yellow → orange → red)

The heatmap is not filled in manually. It is computed from the task bars. That distinction matters when presenting to stakeholders.

---

## Key features

- Single HTML file — open with a double-click, no server, no install, works offline
- Add and manage team members (resources) and tasks from a sidebar panel
- Tasks assigned to a project get an auto-assigned color from a fixed palette
- Three view modes: Gantt only / Heatmap only / Both
- Export and import data as JSON for backup or cross-device sync
- Data persists in `localStorage` between sessions

---

## Tech stack

| Layer | Choice |
|---|---|
| UI framework | React 18 (CDN) |
| JSX compilation | Babel standalone (in-browser) |
| Styling | Inline styles, dark theme (`#0A0F1E`) |
| Persistence | `localStorage` (key: `pm-gantt-v2`) |
| Dependencies | None — fully self-contained |

---

## Getting started

1. Download `pm-workload-board.html`
2. Open it in any modern browser
3. Add your team members under **Risorse**, then add tasks
4. Switch between Gantt, Heatmap, and Both views using the header buttons

No build step. No package manager. No network required after the file is on disk.

---

## Data structure

Data is stored in `localStorage` under the key `pm-gantt-v2` as JSON:

```json
{
  "t": [
    {
      "id": "timestamp string",
      "taskName": "Task name",
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
    "Project name": "#HEX color"
  }
}
```

Use **Export JSON** to download a backup and **Import JSON** to restore it on another device.

---

## Status

Work in progress — features are being actively developed. See the [handoff document](pm-workload-board-handoff.md) for the prioritized roadmap.

---

## Author

**Danilo Magro** — [linkedin.com/in/danilo-magro](https://www.linkedin.com/in/danilo-magro/)

Built via AI-assisted development with [Claude](https://anthropic.com) (Anthropic). Conceived by a human, coded by AI.

---

## License

[MIT](LICENSE) © 2026 Danilo Magro
