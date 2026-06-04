PROJECT-ARCHITECTURE.md

Project Name

CNC Cell Planner PWA

Purpose

Production planning and scheduling tool for CNC job shops.

This application models real manufacturing flow.

Primary Focus

- Travelers / Work Orders
- Operations
- Move Quantities
- Machine Assignments
- Production Tracking
- Dispatching
- Capacity Planning
- Bottleneck Detection
- Scheduling

Long-Term Vision

Calculator
→ Production Tracker
→ Dispatcher
→ Finite Capacity Scheduler
→ Digital Twin of a CNC Cell

Features That Belong Here

- Travelers
- Operation Routing
- Release Quantities
- Machine Queues
- Capacity Forecasting
- Completion Predictions
- Timeline Views
- Gantt/Swimlane Views

Features That Do NOT Belong Here

- G-code Generation
- Tool Libraries
- Speeds & Feeds References
- Drill/Tap Charts
- Geometry Calculators
- Machinist Handbook Features

Those belong in CNC Work Helper.

Development Philosophy

Build the scheduling engine first.

Visualizations come later.

Model reality before adding charts.