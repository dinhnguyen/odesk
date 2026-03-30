# Feature Specification: IT Helpdesk Plugin for Odoo

**Feature Branch**: `001-it-helpdesk-plugin`
**Created**: 2026-03-30
**Status**: Draft
**Input**: User description: "tạo một plugin IT helpdesk dành cho Odoo"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Submit an IT Support Ticket (Priority: P1)

An employee encounters an IT issue (broken laptop, software crash,
password reset, network problem). They navigate to the IT Helpdesk
menu in Odoo, fill in a short form with the issue category, subject,
description, and priority, then submit. The system assigns a ticket
number and notifies the IT team. The employee can track their ticket
status from their portal dashboard.

**Why this priority**: Ticket submission is the core value proposition.
Without it, no other helpdesk functionality matters. This delivers an
immediately usable MVP.

**Independent Test**: Can be fully tested by creating a ticket from
the backend and verifying it appears in the kanban board with correct
status, assignee notification, and ticket number.

**Acceptance Scenarios**:

1. **Given** an authenticated employee in Odoo, **When** they navigate
   to IT Helpdesk > New Ticket and fill in category, subject, and
   description, **Then** a new ticket is created with status "New",
   an auto-generated sequence number, and the submitter receives a
   confirmation email.
2. **Given** a submitted ticket, **When** the IT team views the
   helpdesk kanban board, **Then** the ticket appears in the "New"
   column showing subject, priority, category, and submitter name.
3. **Given** a submitted ticket, **When** the submitter visits the
   website portal, **Then** they can see their ticket with current
   status and any messages from the IT team.

---

### User Story 2 - Manage and Resolve Tickets (Priority: P2)

An IT support agent opens the helpdesk kanban board, sees incoming
tickets, assigns a ticket to themselves (or is auto-assigned), moves
it through stages (New → In Progress → Waiting → Resolved → Closed),
adds internal notes and public replies, and eventually resolves the
ticket. The submitter is notified at each stage change.

**Why this priority**: Without ticket management workflow, submitted
tickets go nowhere. This enables the IT team to actually process and
resolve issues.

**Independent Test**: Can be tested by creating a ticket, assigning
it, moving it through all stages, and verifying notifications are sent
at each transition.

**Acceptance Scenarios**:

1. **Given** a ticket in "New" status, **When** an IT agent clicks
   "Assign to Me", **Then** the ticket is assigned to that agent,
   status changes to "In Progress", and the submitter receives a
   notification.
2. **Given** an assigned ticket, **When** the agent adds a public
   reply, **Then** the submitter receives an email with the reply
   content and can respond via email to update the ticket.
3. **Given** a ticket in any active stage, **When** the agent drags
   it to "Resolved" on the kanban board, **Then** the status updates,
   the submitter is notified, and the resolution time is recorded.
4. **Given** a resolved ticket with no further activity, **When** a
   configurable period passes (default: 7 days), **Then** the ticket
   automatically moves to "Closed" status.
5. **Given** a ticket in "Resolved" or "Closed" status, **When** the
   submitter or an agent clicks "Reopen", **Then** the ticket moves
   back to "In Progress" with the original assignee and SLA timers
   restart.

---

### User Story 3 - SLA Tracking and Escalation (Priority: P3)

An IT manager defines SLA policies (e.g., critical tickets must be
responded to within 1 hour and resolved within 4 hours). The system
tracks SLA compliance per ticket. When an SLA is about to be breached,
the system sends escalation notifications to the team lead. The
manager can view an SLA compliance dashboard showing metrics across
all ticket categories.

**Why this priority**: SLA tracking transforms the helpdesk from a
simple ticket tracker into a service management tool. It enables
accountability and continuous improvement but is not required for
basic ticket flow.

**Independent Test**: Can be tested by creating an SLA policy,
submitting a ticket that matches it, and verifying the SLA timer
starts, deadline is calculated, and escalation triggers when the
deadline approaches.

**Acceptance Scenarios**:

1. **Given** an SLA policy "Critical tickets: respond within 1 hour",
   **When** a critical ticket is submitted, **Then** the system
   calculates and displays the response deadline on the ticket.
2. **Given** a ticket approaching its SLA deadline (within 80% of
   elapsed time), **When** the deadline is near, **Then** the system
   sends a warning notification to the assigned agent and their
   team lead.
3. **Given** a ticket that has breached its SLA, **When** the IT
   manager opens the SLA dashboard, **Then** the ticket appears
   highlighted as breached with the overdue duration shown.

---

### User Story 4 - IT Helpdesk Dashboard and Reporting (Priority: P4)

An IT manager opens the helpdesk dashboard to see an overview of
team performance: open tickets by category, average resolution time,
SLA compliance rate, tickets per agent, and trend over time. They
can filter by date range, category, and team member.

**Why this priority**: Reporting enables data-driven decisions and
justifies IT staffing. It builds on all previous stories and is a
management layer, not a core operational need.

**Independent Test**: Can be tested by creating multiple tickets
in various states and categories, then verifying the dashboard
displays correct aggregated metrics.

**Acceptance Scenarios**:

1. **Given** multiple tickets in various states, **When** the IT
   manager opens the dashboard, **Then** they see total open tickets,
   tickets by category (pie/bar chart), average resolution time, and
   SLA compliance percentage.
2. **Given** the dashboard is open, **When** the manager filters by
   date range "Last 30 days", **Then** all metrics update to reflect
   only tickets within that period.

---

### User Story 5 - Portal Ticket Submission (Priority: P5)

An employee (or external user with portal access) submits an IT
support ticket directly from the Odoo website portal without needing
backend access. They can view their submitted tickets, add follow-up
messages, and see resolution status — all from the portal interface.

**Why this priority**: Portal access removes the dependency on backend
access for ticket submission, making the helpdesk accessible to all
employees including those who don't use Odoo daily. Builds on US1's
core ticket model.

**Independent Test**: Can be tested by logging into the portal as a
non-backend user, submitting a ticket, and verifying it appears in
both the portal view and the backend kanban board.

**Acceptance Scenarios**:

1. **Given** a portal user logged into the Odoo website, **When** they
   navigate to "My Tickets" and click "New Ticket", **Then** they see
   a form with category, subject, description, and priority fields.
2. **Given** a portal-submitted ticket, **When** the IT team updates
   the ticket in the backend, **Then** the portal user sees the
   updated status and messages on the portal page.

---

### Edge Cases

- What happens when a ticket is submitted without a category? The
  system MUST require a category selection; it defaults to "General"
  if the category list is empty.
- What happens when the assigned IT agent is deactivated or leaves
  the company? Tickets assigned to a deactivated user MUST be
  automatically reassigned to the team's default queue.
- What happens when an SLA policy is modified while tickets are
  already in progress? Existing tickets MUST retain the SLA terms
  that were active at the time of their creation.
- How does the system handle duplicate ticket submissions? The system
  SHOULD detect and warn when a user submits a ticket with an
  identical subject within the last 24 hours, but still allow
  submission.
- What happens when the email server is unreachable? Ticket creation
  MUST succeed even if email notification fails; failed notifications
  MUST be queued for retry.
- What happens when a resolved or closed issue recurs? The submitter
  or an agent can reopen the ticket, which moves it back to
  "In Progress" with the original assignee (if still active).
  SLA timers restart from the reopening moment.

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST provide a helpdesk ticket model with fields:
  sequence number, subject, description, category, priority
  (low/medium/high/critical), status, submitter, assignee, and
  timestamps (created, assigned, resolved, closed).
- **FR-002**: System MUST provide configurable ticket stages (New,
  In Progress, Waiting for User, Resolved, Closed) displayed as a
  kanban board.
- **FR-003**: System MUST support ticket categories (Hardware,
  Software, Network, Access/Permissions, General) that are
  user-configurable by the IT manager.
- **FR-004**: System MUST send email notifications on: ticket
  creation (to IT team), assignment (to submitter), stage changes
  (to submitter), and new messages (to relevant parties).
- **FR-005**: System MUST provide email-based ticket updates via
  `mail.thread` integration — replies to notification emails MUST
  create messages on the corresponding ticket.
- **FR-006**: System MUST support ticket assignment: manual
  (agent self-assigns or manager assigns) and automatic
  (round-robin among available agents in the team).
- **FR-007**: System MUST track SLA policies with configurable
  response time and resolution time per priority level.
- **FR-008**: System MUST send escalation notifications when SLA
  deadlines are approaching (configurable warning threshold,
  default 80% of elapsed time).
- **FR-009**: System MUST provide a dashboard view showing: open
  ticket count, tickets by category, tickets by priority, average
  resolution time, and SLA compliance rate.
- **FR-010**: System MUST provide a website portal interface for
  ticket submission, tracking, and messaging by portal users.
- **FR-011**: System MUST support file attachments on tickets
  (screenshots, logs, documents) with a configurable maximum file
  size.
- **FR-012**: System MUST auto-close resolved tickets after a
  configurable inactivity period (default: 7 days).
- **FR-013**: System MUST maintain a complete audit trail of all
  ticket changes (stage transitions, assignments, field edits)
  via the chatter/log.
- **FR-014**: System MUST support IT helpdesk teams, allowing
  tickets to be routed to specific teams based on category.
  Agents and managers MUST be able to transfer a ticket to a
  different team (reassigning team, category, and optionally
  the assignee). Transfers MUST be logged in the audit trail.
- **FR-015**: System MUST define three security groups with
  inherited permissions: Helpdesk User (submit and view own
  tickets), Helpdesk Agent (manage assigned tickets, view team
  tickets, add replies/notes), Helpdesk Manager (full access
  including SLA configuration, team management, reporting, and
  all ticket operations).

### Key Entities

- **Ticket**: The core entity representing an IT support request.
  Key attributes: sequence number, subject, description, category,
  priority, status/stage, submitter (employee/portal user), assigned
  agent, team, SLA deadline, timestamps, attachments, messages.
- **Ticket Category**: Configurable classification for tickets
  (e.g., Hardware, Software, Network). Linked to teams for routing.
- **Ticket Stage**: Configurable workflow stages that tickets move
  through. Key attributes: name, sequence order, fold state
  (for kanban), is-closing flag.
- **SLA Policy**: Defines response and resolution time targets per
  priority level. Key attributes: name, priority, response time,
  resolution time, team.
- **Helpdesk Team**: A group of IT agents that handle tickets for
  specific categories. Key attributes: name, members, assignment
  method (manual/round-robin), default SLA policy.
- **Security Group**: Three-tier permission hierarchy — Helpdesk
  User (submit/view own), Helpdesk Agent (inherits User + manage
  assigned/team tickets), Helpdesk Manager (inherits Agent + full
  access to configuration, SLA, teams, and reporting).

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Employees can submit a new IT support ticket in under
  60 seconds (3 clicks and a short form).
- **SC-002**: IT agents can view and triage all new tickets within
  a single kanban board without navigating to separate pages.
- **SC-003**: 100% of ticket stage transitions generate submitter
  notifications within 5 minutes.
- **SC-004**: SLA compliance is tracked with visible countdown on
  each ticket, and escalation notifications fire before breach.
- **SC-005**: IT managers can view team performance dashboard with
  key metrics (open tickets, resolution time, SLA compliance)
  without exporting data or running manual queries.
- **SC-006**: Portal users can submit and track tickets without
  requiring Odoo backend access.
- **SC-007**: Auto-close of resolved tickets reduces manual ticket
  management overhead by eliminating the need to manually close
  stale tickets.

## Clarifications

### Session 2026-03-30

- Q: Should time tracking (agents log hours per ticket) be included? → A: Defer to v2 — keep as future scope, remove from current US2.
- Q: What security group hierarchy should the module define? → A: Three groups — Helpdesk User (submit/view own), Agent (manage assigned), Manager (full access).
- Q: Can closed or resolved tickets be reopened? → A: Yes, both Resolved and Closed tickets can be reopened — moves ticket back to "In Progress".
- Q: Can tickets be transferred between teams after creation? → A: Yes, agents and managers can reassign a ticket to a different team.
- Q: Should the module include canned/template responses for agents? → A: No, exclude from v1 — agents type replies manually.

## Assumptions

- Odoo 18.0 (Community or Enterprise) is the target platform; the
  module will use only core module dependencies (`mail`, `portal`,
  `base`, `web`).
- Users are authenticated via Odoo's built-in authentication; no
  external SSO integration is needed for v1.
- The Odoo email server (`ir.mail_server`) is already configured
  and operational for sending notifications.
- The module targets small-to-medium IT teams (1-20 agents) and
  organizations with up to 500 employees submitting tickets.
- Mobile responsiveness is handled by Odoo's default responsive
  layout; no custom mobile app is in scope for v1.
- Multilingual support is provided via Odoo's standard `_()`
  translation mechanism; no custom translation workflow is needed.
- SLA time calculations use business hours (Monday-Friday,
  configurable working schedule); 24/7 SLA is out of scope for v1.
- Integration with external ITSM tools (ServiceNow, Jira Service
  Management) is out of scope for v1.
- Time tracking (agent hours logged per ticket) is deferred to v2.
- Canned/template responses for agents are out of scope for v1.
