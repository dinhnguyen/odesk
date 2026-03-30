# Research: IT Helpdesk Plugin for Odoo

**Date**: 2026-03-30
**Branch**: `001-it-helpdesk-plugin`

## Technology Decisions

### 1. Odoo Version & Python Runtime

- **Decision**: Odoo 18.0 with Python 3.10+
- **Rationale**: User requirement. Odoo 18.0 is the current stable
  release with long-term support. Python 3.10+ is the minimum
  supported runtime.
- **Alternatives considered**: Odoo 17.0 (previous LTS, rejected
  per user preference).

### 2. Module Dependencies

- **Decision**: `base`, `mail`, `portal`, `web` (core modules only)
- **Rationale**: Constitution mandates no community module deps.
  `mail` provides `mail.thread` and `mail.activity.mixin` for
  chatter, email integration, and activity scheduling. `portal`
  provides the website portal framework for ticket submission by
  non-backend users. `web` is required for kanban and dashboard views.
- **Alternatives considered**: `website` module (rejected — `portal`
  is sufficient for ticket portal; `website` adds unnecessary
  complexity for CMS features not needed).

### 3. SLA Time Computation Approach

- **Decision**: Cron-based SLA deadline checking with computed fields
  for real-time display.
- **Rationale**: SLA deadlines are computed at ticket creation/stage
  change and stored as datetime fields. A scheduled action (cron)
  runs periodically (every 15 minutes) to check for approaching
  and breached SLAs, triggering escalation notifications. Computed
  fields on the ticket model provide real-time remaining time for
  the UI.
- **Alternatives considered**:
  - Real-time OWL widget with countdown (rejected — adds frontend
    complexity; Odoo's standard field rendering with cron is
    sufficient for the target scale).
  - Queue-based job scheduling (rejected — requires `queue_job`
    community module, violates dependency constraint).

### 4. Auto-Assignment Strategy

- **Decision**: Round-robin based on `last_assignment_date` per
  team member.
- **Rationale**: Track a `last_assignment_date` field on
  `helpdesk.team` member records. On auto-assignment, select the
  team member with the oldest (or null) `last_assignment_date`.
  This ensures even distribution without complex load-balancing.
- **Alternatives considered**:
  - Workload-based (count of open tickets per agent) — more
    accurate but adds query overhead and doesn't account for
    ticket complexity. Deferred to v2.
  - Random assignment — simple but unfair distribution.

### 5. Auto-Close Mechanism

- **Decision**: Scheduled action (cron) that runs daily to close
  resolved tickets past the inactivity threshold.
- **Rationale**: A cron job queries tickets in "Resolved" stage
  where `write_date` is older than the configurable threshold
  (default 7 days). Simple, reliable, and standard Odoo pattern.
- **Alternatives considered**: Mail activity-based reminder
  (rejected — over-engineered for a simple time-based check).

### 6. Dashboard Implementation

- **Decision**: Odoo native graph views + pivot views with a
  dedicated dashboard action.
- **Rationale**: Odoo 18.0's built-in graph and pivot views
  support pie charts, bar charts, line charts, and filtering.
  A dashboard action combining multiple graph views provides
  the required metrics without custom OWL development.
- **Alternatives considered**: Custom OWL dashboard component
  (rejected — adds significant frontend complexity; native views
  are sufficient for the defined success criteria).

### 7. Portal Implementation

- **Decision**: Standard `portal.mixin` + QWeb portal templates
  with controller routes.
- **Rationale**: `portal.mixin` provides `access_url` and
  `_get_report_base_filename` automatically. QWeb templates
  extend `portal.portal` to add "My Tickets" to the portal
  navigation. Controller handles form submission and list/detail
  views.
- **Alternatives considered**: Odoo Website form builder
  (rejected — less control over field validation and ticket
  routing logic).

### 8. Ticket Sequence

- **Decision**: `ir.sequence` with prefix `HD` and padding 5
  (e.g., `HD00001`).
- **Rationale**: Standard Odoo pattern for auto-incrementing
  document numbers. Configurable by the user via the sequence
  settings UI.
- **Alternatives considered**: Custom sequence logic (rejected —
  `ir.sequence` is the canonical Odoo approach).

## No Unresolved Items

All technical decisions are resolved. No NEEDS CLARIFICATION
items remain from the Technical Context.
