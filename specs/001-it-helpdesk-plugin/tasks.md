# Tasks: IT Helpdesk Plugin for Odoo

**Input**: Design documents from `/specs/001-it-helpdesk-plugin/`
**Prerequisites**: plan.md (required), spec.md (required), research.md, data-model.md, contracts/

**Tests**: Not explicitly requested in the feature specification. Test tasks are excluded.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Odoo addon**: `odesk_helpdesk/` at repository root

---

## Phase 1: Setup

**Purpose**: Module scaffold and project initialization

- [x] T001 Create module directory structure with `odesk_helpdesk/__init__.py`
- [x] T002 Create `odesk_helpdesk/__manifest__.py` with name "IT Helpdesk", version `18.0.1.0.0`, depends `['base', 'mail', 'portal', 'web']`, and all data/view/security file references
- [x] T003 [P] Create `odesk_helpdesk/models/__init__.py` importing all model modules
- [x] T004 [P] Create `odesk_helpdesk/controllers/__init__.py` importing portal controller
- [x] T005 [P] Add module icon at `odesk_helpdesk/static/description/icon.png`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Shared models, security, and base data that ALL user stories depend on

**CRITICAL**: No user story work can begin until this phase is complete

- [x] T006 Create `helpdesk.stage` model in `odesk_helpdesk/models/helpdesk_stage.py` with fields: name (Char, required, translate), sequence (Integer), fold (Boolean), is_close (Boolean), is_done (Boolean), description (Text)
- [x] T007 [P] Create `helpdesk.category` model in `odesk_helpdesk/models/helpdesk_category.py` with fields: name (Char, required, translate), team_id (Many2one), description (Text), sequence (Integer), active (Boolean)
- [x] T008 [P] Create `helpdesk.tag` model in `odesk_helpdesk/models/helpdesk_tag.py` with fields: name (Char, required, unique), color (Integer)
- [x] T009 Create `helpdesk.team` model in `odesk_helpdesk/models/helpdesk_team.py` with fields: name (Char, required), description (Text), member_ids (Many2many res.users), leader_id (Many2one res.users), assignment_method (Selection manual/round_robin), category_ids (One2many), sla_policy_ids (One2many), ticket_ids (One2many), auto_close_days (Integer default=7), color (Integer), active (Boolean)
- [x] T010 Create security groups (Helpdesk User, Agent, Manager) with inheritance chain in `odesk_helpdesk/security/helpdesk_security.xml`
- [x] T011 Create `odesk_helpdesk/security/ir.model.access.csv` with access rights for all models per security group
- [x] T012 [P] Create default stage data (New, In Progress, Waiting for User, Resolved, Closed) with noupdate="1" in `odesk_helpdesk/data/helpdesk_stage_data.xml`
- [x] T013 [P] Create default category data (Hardware, Software, Network, Access/Permissions, General) with noupdate="1" in `odesk_helpdesk/data/helpdesk_category_data.xml`
- [x] T014 Create stage configuration views (form, tree) in `odesk_helpdesk/views/helpdesk_stage_views.xml`
- [x] T015 [P] Create category configuration views (form, tree) in `odesk_helpdesk/views/helpdesk_category_views.xml`
- [x] T016 [P] Create team configuration views (form, tree) with member management in `odesk_helpdesk/views/helpdesk_team_views.xml`

**Checkpoint**: Foundation ready — models, security, and base data installed. User story implementation can begin.

---

## Phase 3: User Story 1 — Submit an IT Support Ticket (Priority: P1) MVP

**Goal**: Employees can create tickets via backend with auto-sequencing, email notification, and kanban view.

**Independent Test**: Create a ticket from the backend, verify it appears in kanban with correct number, stage "New", and confirmation email is sent.

### Implementation for User Story 1

- [x] T017 [US1] Create ticket sequence (prefix HD, padding 5) in `odesk_helpdesk/data/helpdesk_sequence_data.xml`
- [x] T018 [US1] Create `helpdesk.ticket` model in `odesk_helpdesk/models/helpdesk_ticket.py` with all fields from data-model.md, inheriting `mail.thread`, `mail.activity.mixin`, `portal.mixin`; implement `create()` override for sequence number assignment and team routing from category
- [x] T019 [US1] Add record rules for ticket visibility (User sees own, Agent sees team, Manager sees all) in `odesk_helpdesk/security/helpdesk_security.xml`
- [x] T020 [US1] Update `odesk_helpdesk/security/ir.model.access.csv` with `helpdesk.ticket` access rights per group
- [x] T021 [US1] Create ticket creation email template (confirmation to submitter, notification to team) in `odesk_helpdesk/data/helpdesk_mail_template_data.xml`
- [x] T022 [US1] Create ticket views (form with chatter, kanban with priority/category/assignee, tree, search with filters/groupby) in `odesk_helpdesk/views/helpdesk_ticket_views.xml`
- [x] T023 [US1] Create menu structure (IT Helpdesk root, Tickets, Configuration submenu with Teams/Categories/Stages) and window actions in `odesk_helpdesk/views/helpdesk_menus.xml`
- [x] T024 [US1] Create demo data with 1 team, 3 agents, 2 SLA policies, 10 sample tickets in various stages in `odesk_helpdesk/demo/helpdesk_demo.xml`

**Checkpoint**: US1 complete — tickets can be created, viewed in kanban, and confirmation emails are sent. MVP functional.

---

## Phase 4: User Story 2 — Manage and Resolve Tickets (Priority: P2)

**Goal**: Agents can assign, transition stages, reply, reopen, and auto-close resolved tickets.

**Independent Test**: Create a ticket, assign it, move through all stages, verify notifications at each transition, reopen a closed ticket, verify auto-close cron works.

### Implementation for User Story 2

- [x] T025 [US2] Implement manual assignment (`assign_to_me` button action) and round-robin auto-assignment logic (`_assign_ticket_round_robin` method) in `odesk_helpdesk/models/helpdesk_team.py`
- [x] T026 [US2] Implement `write()` override on `helpdesk.ticket` in `odesk_helpdesk/models/helpdesk_ticket.py` to track stage transitions: set `date_assigned` on first assignment, `date_resolved` when entering is_done stage, `date_closed` when entering is_close stage, `date_last_stage_update` on any stage change; send notification emails on stage change
- [x] T027 [US2] Implement `action_reopen` method on `helpdesk.ticket` in `odesk_helpdesk/models/helpdesk_ticket.py` to move ticket back to "In Progress" stage, clear resolved/closed dates, and restart SLA timers
- [x] T028 [US2] Add stage change and assignment email templates (agent assigned, stage changed, ticket resolved) in `odesk_helpdesk/data/helpdesk_mail_template_data.xml`
- [x] T029 [US2] Create auto-close cron job (daily, searches resolved tickets past `auto_close_days` threshold, moves to Closed stage) in `odesk_helpdesk/data/helpdesk_cron_data.xml`
- [x] T030 [US2] Implement `_cron_auto_close_tickets` method on `helpdesk.ticket` in `odesk_helpdesk/models/helpdesk_ticket.py`
- [x] T031 [US2] Add "Assign to Me" and "Reopen" buttons to ticket form view, update kanban view with drag-and-drop stage transitions in `odesk_helpdesk/views/helpdesk_ticket_views.xml`

**Checkpoint**: US1 + US2 complete — full ticket lifecycle works: create, assign, transition, reply, reopen, auto-close.

---

## Phase 5: User Story 3 — SLA Tracking and Escalation (Priority: P3)

**Goal**: Managers define SLA policies; system tracks deadlines per ticket and sends escalation notifications on approaching breach.

**Independent Test**: Create an SLA policy, submit a matching ticket, verify deadline is computed, let time pass (or manipulate dates), verify escalation notification fires.

### Implementation for User Story 3

- [x] T032 [P] [US3] Create `helpdesk.sla.policy` model in `odesk_helpdesk/models/helpdesk_sla.py` with fields from data-model.md: name, team_id, priority, category_ids, time_response, time_resolution, stage_id, active
- [x] T033 [P] [US3] Create `helpdesk.sla.status` model in `odesk_helpdesk/models/helpdesk_sla_status.py` with fields: ticket_id, sla_policy_id, deadline (computed from policy + ticket creation time), reached, failed, reached_date, exceeded_hours (computed)
- [x] T034 [US3] Implement SLA application logic on `helpdesk.ticket` in `odesk_helpdesk/models/helpdesk_ticket.py`: on create/write, find matching SLA policies for ticket's team+priority+category, create `helpdesk.sla.status` records, compute `sla_deadline` (earliest deadline), update `sla_reached`/`sla_failed` on stage transitions
- [x] T035 [US3] Create SLA escalation cron job (every 15 minutes, checks tickets approaching SLA deadline at 80% threshold, sends warning to agent + team leader) in `odesk_helpdesk/data/helpdesk_cron_data.xml`
- [x] T036 [US3] Implement `_cron_sla_escalation` method on `helpdesk.ticket` in `odesk_helpdesk/models/helpdesk_ticket.py`
- [x] T037 [US3] Add SLA escalation email template (warning to agent, escalation to team lead) in `odesk_helpdesk/data/helpdesk_mail_template_data.xml`
- [x] T038 [P] [US3] Create SLA policy views (form, tree) in `odesk_helpdesk/views/helpdesk_sla_views.xml`
- [x] T039 [US3] Add SLA deadline, SLA status indicators, and SLA failed/reached badges to ticket form and kanban views in `odesk_helpdesk/views/helpdesk_ticket_views.xml`
- [x] T040 [US3] Add SLA Policies menu item under Configuration in `odesk_helpdesk/views/helpdesk_menus.xml`
- [x] T041 [US3] Update `odesk_helpdesk/security/ir.model.access.csv` with access rights for `helpdesk.sla.policy` and `helpdesk.sla.status` models

**Checkpoint**: US1 + US2 + US3 complete — tickets track SLA deadlines, escalation fires before breach.

---

## Phase 6: User Story 4 — Dashboard and Reporting (Priority: P4)

**Goal**: IT managers view aggregated metrics: open tickets, tickets by category/priority, average resolution time, SLA compliance rate.

**Independent Test**: With existing demo tickets, open the dashboard and verify graphs display correct aggregated data with working filters.

### Implementation for User Story 4

- [x] T042 [US4] Create dashboard views with graph (bar: tickets by category, pie: tickets by priority, line: tickets over time) and pivot (resolution time by agent/category) views in `odesk_helpdesk/views/helpdesk_dashboard_views.xml`
- [x] T043 [US4] Add computed fields for dashboard metrics on `helpdesk.ticket` in `odesk_helpdesk/models/helpdesk_ticket.py`: `resolution_hours` (Float, computed from date_created to date_resolved), `is_sla_compliant` (Boolean, computed from sla_status_ids)
- [x] T044 [US4] Add Dashboard menu item with window action combining graph views in `odesk_helpdesk/views/helpdesk_menus.xml`

**Checkpoint**: US1-US4 complete — managers can view performance metrics and SLA compliance.

---

## Phase 7: User Story 5 — Portal Ticket Submission (Priority: P5)

**Goal**: Portal users can submit, view, and reply to tickets from the Odoo website portal.

**Independent Test**: Log in as a portal user, submit a ticket, verify it appears in backend kanban; add a reply from portal, verify it appears as a message on the ticket.

### Implementation for User Story 5

- [x] T045 [US5] Implement `_compute_access_url` on `helpdesk.ticket` in `odesk_helpdesk/models/helpdesk_ticket.py` to return `/my/helpdesk/<ticket_id>`
- [x] T046 [US5] Create portal controller in `odesk_helpdesk/controllers/portal.py` with routes: GET `/my/helpdesk` (list), GET `/my/helpdesk/<int:ticket_id>` (detail), GET `/my/helpdesk/new` (form), POST `/my/helpdesk/new` (submit), POST `/my/helpdesk/<int:ticket_id>/reply` (reply); implement access checks (partner_id match), pagination, sorting, search
- [x] T047 [US5] Create portal QWeb templates in `odesk_helpdesk/views/portal_templates.xml`: ticket list page extending `portal.portal` with "My Tickets" navigation entry, ticket detail page with chatter messages and reply form, new ticket form with category/subject/description/priority/attachment fields
- [x] T048 [US5] Add portal access rules for `helpdesk.ticket` (portal users see own tickets via partner_id) in `odesk_helpdesk/security/helpdesk_security.xml`
- [x] T049 [US5] Update `odesk_helpdesk/security/ir.model.access.csv` with read access for portal group on ticket, stage, and category models

**Checkpoint**: All user stories complete — full helpdesk functionality including portal.

---

## Phase 8: Polish & Cross-Cutting Concerns

**Purpose**: Final refinements across all user stories

- [x] T050 [P] Verify all translatable strings use `_()` in Python and `translate="True"` on Char fields across all model files in `odesk_helpdesk/models/`
- [x] T051 [P] Verify `__manifest__.py` includes all data, view, security, and demo files in correct load order in `odesk_helpdesk/__manifest__.py`
- [ ] T052 Validate module installs cleanly on a fresh Odoo 18.0 database (run `odoo-bin -i odesk_helpdesk -d test_db --stop-after-init`)
- [x] T053 [P] Review and finalize demo data completeness (tickets in all stages, SLA breached/met examples, multiple categories) in `odesk_helpdesk/demo/helpdesk_demo.xml`
- [x] T054 Verify all security rules work correctly: User sees only own tickets, Agent sees team tickets, Manager sees all; portal users see only own tickets

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies — can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion — BLOCKS all user stories
- **US1 (Phase 3)**: Depends on Foundational phase — MVP delivery
- **US2 (Phase 4)**: Depends on US1 (ticket model must exist)
- **US3 (Phase 5)**: Depends on US1 (ticket model must exist); T032/T033 can start in parallel with US2
- **US4 (Phase 6)**: Depends on US1 + US3 (needs SLA fields on ticket)
- **US5 (Phase 7)**: Depends on US1 (ticket model must exist); can run in parallel with US2/US3
- **Polish (Phase 8)**: Depends on all user stories being complete

### User Story Dependencies

- **US1 (P1)**: Can start after Foundational (Phase 2) — No dependencies on other stories
- **US2 (P2)**: Depends on US1 ticket model — extends ticket with assignment/stage logic
- **US3 (P3)**: Depends on US1 ticket model — adds SLA models and computation; T032/T033 (model files) can start in parallel with US2
- **US4 (P4)**: Depends on US1 + US3 — dashboard uses SLA compliance fields
- **US5 (P5)**: Depends on US1 ticket model — can run in parallel with US2/US3/US4

### Within Each User Story

- Models before views
- Data files before views that reference them
- Security updates before testing
- Core logic before UI integration

### Parallel Opportunities

- Phase 1: T003, T004, T005 can run in parallel
- Phase 2: T007+T008 in parallel; T012+T013 in parallel; T014+T015+T016 in parallel
- Phase 5: T032+T033 in parallel; T038 in parallel with T034
- US3 model creation (T032/T033) can start in parallel with US2 implementation
- US5 (Phase 7) can start in parallel with US3/US4 after US1 completes

---

## Implementation Strategy

### MVP First (User Story 1 Only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL — blocks all stories)
3. Complete Phase 3: User Story 1
4. **STOP and VALIDATE**: Install module, create a ticket, verify kanban and email
5. Deploy/demo if ready

### Incremental Delivery

1. Setup + Foundational → Foundation ready
2. Add US1 → Test independently → Deploy (MVP!)
3. Add US2 → Test independently → Deploy (ticket management)
4. Add US3 → Test independently → Deploy (SLA tracking)
5. Add US4 → Test independently → Deploy (dashboard)
6. Add US5 → Test independently → Deploy (portal)
7. Polish → Final validation → Release

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once US1 is done:
   - Developer A: US2 (ticket management)
   - Developer B: US3 models (T032/T033) + US5 (portal)
3. After US3 models ready:
   - Developer A: US3 logic (T034-T041)
   - Developer B: US4 (dashboard, needs US3 SLA fields)
4. Polish phase: team together

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
