# CNC Cell Planner PWA

A lightweight offline-capable production planner for CNC machining cells, job shops, and small manufacturing teams.

The project started as a cycle-time calculator and is evolving into a shop-floor production tracker. The current focus is traveler flow: where each work order is, what operation is next, and when downstream work can begin.

## Current Features

- Job setup with part number, job number, quantity, shifts, breaks, dates, and shop holidays
- U.S. government holiday preload with editable/removable closure dates
- Operation routing with cycle time, setup time, machine/station, type, and Move Qty
- Travelers / Work Orders with WO number, quantity, current operation, status, operation progress, and advance control
- Move Qty release logic so downstream operations only become eligible after enough pieces are completed at the current operation
- Completed operation history per traveler
- Traveler summary showing how many travelers are at each operation and how many are complete
- Progress tracker and bottleneck reality check
- Tooling tracker with usage and order estimates
- Reports tab with operation hours, bottleneck hours, work order totals, and machine hours
- Assistant tab with Google Gemini, OpenAI, Anthropic Claude, xAI Grok, and Groq API key support
- Export backup to JSON
- Import backup from JSON
- Reset flow with backup option
- LocalStorage persistence
- Offline PWA support for GitHub Pages

## Traveler Flow

Travelers move through the sorted operation list.

Example route:

```text
OP10 -> OP20 -> OP30 -> OP40 -> COMPLETE
```

Each traveler tracks:

- WO number
- Quantity
- Current operation
- Done quantity at the current operation
- Completed operations
- Next operation
- Status: Not Started, In Process, Complete, or Hold

## Move Qty Logic

Operations include a `Move Qty` field.

Example:

```text
OP20 Move Qty = 10
```

That means OP30 should not be released until at least 10 pieces are completed at OP20.

In Travelers, enter the completed amount in `Done @ Op`. Once the completed amount reaches the operation's Move Qty, the Advance button becomes available.

This supports real shop flow such as:

```text
Run 10 pieces at OP20
Start OP30 while OP20 continues running
```

## Backup And Recovery

The app stores data locally in the browser and supports JSON backup files.

Use:

- `Export` before major changes or testing
- `Import` to restore a saved job
- `Reset` to clear the app, with a backup prompt first

Backups include job data, operations, tooling, holidays, travelers, current operation, completed operation history, and operation progress.

## PWA Notes

This app is designed to run from GitHub Pages and work offline after installation.

Core files:

- `index.html`
- `manifest.json`
- `sw.js`
- `icons/`

When publishing updates, GitHub Pages and the browser service worker may take a moment to refresh. If the live site looks old, close/reopen the PWA or clear site data for the GitHub Pages site.

## Roadmap

Near-term:

- Improve phone-friendly Traveler layout
- Add clearer release/ready indicators
- Add simple machine queue view

Future phases:

- Bottleneck detection by machine
- Shared machine conflict detection
- "What should I run next?" recommendations
- Capacity scheduling
- Predicted completion dates
- Timeline or swimlane visualization
- What-if simulations

## Development Principle

Build the scheduling engine first.

Visual charts come later. The priority is accurate shop-floor flow modeling: travelers, move quantities, operation release, machine constraints, and bottlenecks.
