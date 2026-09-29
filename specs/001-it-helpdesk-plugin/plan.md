# Implementation Plan: IT Helpdesk Plugin for Odoo

**Branch**: `001-it-helpdesk-plugin` | **Date**: 2026-03-30 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-it-helpdesk-plugin/spec.md`

## Summary

Build an Odoo 18.0 module (`odesk_helpdesk`) that provides a complete
IT helpdesk system: ticket submission with auto-sequencing and email
notifications, kanban-based ticket management with configurable stages,
team-based routing with round-robin assignment, SLA tracking with
escalation, a management dashboard, and a website portal for
non-backend users. The module uses only Odoo core dependencies
(`mail`, `portal`, `base`, `web`) and follows standard Odoo addon
conventions.

## Technical Context

**Language/Version**: Python 3.10+ (Odoo 18.0 runtime)
**Primary Dependencies**: Odoo 18.0 core modules (`base`, `mail`, `portal`, `web`)
**Storage**: PostgreSQL (managed by Odoo ORM)
**Testing**: `odoo.tests.common.TransactionCase`, `odoo.tests.common.HttpCase`, `pylint-odoo`
**Target Platform**: Odoo 18.0 server (Linux/macOS/Docker)
**Project Type**: Odoo addon module
**Performance Goals**: Ticket submission < 60s, notification delivery < 5min, dashboard load < 3s for 10k tickets
**Constraints**: No community module deps, no raw SQL, no private API overrides, ORM-only data access
**Scale/Scope**: 1-20 IT agents, up to 500 employees, ~10k tickets/year

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

| # | Principle | Gate | Status |
|---|-----------|------|--------|
| I | Odoo Module Standards | Module has `__manifest__.py`, `__init__.py`; models use `models.Model`; views are XML `ir.ui.view`; security via CSV + record rules; menus/actions in XML | PASS |
| II | Data Integrity & Security | All models have `ir.model.access.csv` entries; 3-tier security groups with record rules; no raw SQL; QWeb uses `t-esc` | PASS |
| III | User Experience First | Ticket creation ≤ 3 clicks; kanban shows status/priority/assignee; portal support; mail.thread + mail.activity.mixin; dashboard with SLA metrics | PASS |
| IV | Testing & Quality | TransactionCase tests for SLA computation, auto-assignment, escalation; module installs on clean DB; pylint-odoo clean | PASS |
| V | Maintainability & Upgrade Safety | New models (no `_inherit` needed for core); `noupdate="1"` for stages/templates; no community deps; version `18.0.1.0.0` | PASS |

All gates pass. No violations to justify.

## Project Structure

### Documentation (this feature)

```text
specs/001-it-helpdesk-plugin/
├── plan.md              # This file
├── research.md          # Phase 0 output
├── data-model.md        # Phase 1 output
├── quickstart.md        # Phase 1 output
├── contracts/           # Phase 1 output (portal routes)
└── tasks.md             # Phase 2 output (/speckit.tasks)
```

### Source Code (repository root)

```text
odesk_helpdesk/
├── __init__.py
├── __manifest__.py
├── models/
│   ├── __init__.py
│   ├── helpdesk_ticket.py
│   ├── helpdesk_stage.py
│   ├── helpdesk_category.py
│   ├── helpdesk_team.py
│   ├── helpdesk_sla.py
│   └── helpdesk_sla_status.py
├── views/
│   ├── helpdesk_ticket_views.xml
│   ├── helpdesk_stage_views.xml
│   ├── helpdesk_category_views.xml
│   ├── helpdesk_team_views.xml
│   ├── helpdesk_sla_views.xml
│   ├── helpdesk_dashboard_views.xml
│   └── helpdesk_menus.xml
├── security/
│   ├── helpdesk_security.xml
│   └── ir.model.access.csv
├── data/
│   ├── helpdesk_stage_data.xml
│   ├── helpdesk_category_data.xml
│   ├── helpdesk_sequence_data.xml
│   ├── helpdesk_mail_template_data.xml
│   └── helpdesk_cron_data.xml
├── controllers/
│   ├── __init__.py
│   └── portal.py
├── views/
│   └── portal_templates.xml
├── demo/
│   └── helpdesk_demo.xml
├── static/
│   └── description/
│       └── icon.png
└── tests/
    ├── __init__.py
    ├── test_helpdesk_ticket.py
    ├── test_helpdesk_sla.py
    ├── test_helpdesk_assignment.py
    └── test_helpdesk_portal.py
```

**Structure Decision**: Standard Odoo addon module structure at
repository root. All Python models in `models/`, XML views in
`views/`, security definitions in `security/`, default data in
`data/` with `noupdate="1"` for user-customizable records, portal
controllers in `controllers/`, and tests in `tests/`.

## Complexity Tracking

No constitution violations. No complexity justifications needed.
