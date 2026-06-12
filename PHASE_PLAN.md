# CNC Cell Planner Phase Plan

## Summary

CNC Cell Planner is the production planning and shop-flow app. It should continue evolving from a cycle-time calculator into a shop-floor tracker, dispatcher, and finite-capacity planning tool.

Default constraints:

- Keep the app static and offline-capable on GitHub Pages.
- Keep data local with JSON import/export backup.
- Build scheduling engine behavior before adding visual charts.
- Keep CNC Work Helper and Green Hat features out of this app unless they directly support production planning.

## Phase 1: Stabilize Shop-Flow Core

- Lock down Travelers, operations, move quantity release, inspection states, and completed-op history.
- Improve the machine queue view so users can see what is ready, waiting, held, or complete by machine and operation.
- Keep tooling and order reporting as supporting workflow, not the main identity.
- Continue tightening mobile/tablet layouts for shop-floor use.

## Phase 2: Scheduling Engine

- Add machine-level bottleneck detection and shared-machine conflict warnings.
- Improve projected finish dates by operation and traveler batch.
- Add clearer capacity limits when assigned operation shifts cannot meet due dates.
- Add "what should I run next?" recommendations based on readiness, bottleneck, due date, and move quantity.

## Phase 3: Visual Planning

- Add timeline or swimlane views after the scheduling engine is reliable.
- Show traveler movement by operation and machine.
- Surface forecast finish and late-risk areas without hiding the underlying numbers.
- Keep charts explanatory, not decorative.

## Phase 4: Production Ops Polish

- Strengthen import/export backup, print reports, and PWA update behavior.
- Improve status summaries for supervisors and operators.
- Add multi-job dashboard only after single-job flow is stable.

## Acceptance Rules

- Every PWA-facing change that affects cached files must bump the visible version and `sw.js` cache name.
- Every change must preserve offline behavior.
- Every feature must answer a production planning or shop-flow question.
- Before editing, confirm local `main` is clean and aligned with `origin/main`.
