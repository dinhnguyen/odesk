# Data Model: IT Helpdesk Plugin for Odoo

**Date**: 2026-03-30
**Branch**: `001-it-helpdesk-plugin`

## Entity Relationship Overview

```text
helpdesk.team 1───* helpdesk.ticket
helpdesk.team 1───* helpdesk.sla.policy
helpdesk.team *───* res.users (members)
helpdesk.ticket *───1 helpdesk.stage
helpdesk.ticket *───1 helpdesk.category
helpdesk.ticket *───1 res.users (assignee)
helpdesk.ticket *───1 res.partner (submitter)
helpdesk.ticket 1───* helpdesk.sla.status
helpdesk.sla.status *───1 helpdesk.sla.policy
helpdesk.category *───1 helpdesk.team (default routing)
```

## Models

### helpdesk.team

Represents an IT support team with members and configuration.

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| name | Char | Team name | required, unique |
| description | Text | Team description | |
| member_ids | Many2many(res.users) | Team members | |
| leader_id | Many2one(res.users) | Team leader (escalation target) | |
| assignment_method | Selection | `manual` or `round_robin` | required, default='manual' |
| category_ids | One2many(helpdesk.category) | Categories routed to this team | |
| sla_policy_ids | One2many(helpdesk.sla.policy) | SLA policies for this team | |
| ticket_ids | One2many(helpdesk.ticket) | Tickets assigned to this team | |
| auto_close_days | Integer | Days before auto-closing resolved tickets | default=7, min=1 |
| color | Integer | Kanban color index | |
| active | Boolean | Archive flag | default=True |

### helpdesk.ticket

Core entity representing an IT support request.

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| name | Char | Ticket subject | required |
| number | Char | Auto-generated sequence (HD00001) | readonly, copy=False |
| description | Html | Detailed description | |
| partner_id | Many2one(res.partner) | Submitter | required, default=current partner |
| user_id | Many2one(res.users) | Assigned agent | |
| team_id | Many2one(helpdesk.team) | Assigned team | required |
| category_id | Many2one(helpdesk.category) | Ticket category | required |
| stage_id | Many2one(helpdesk.stage) | Current stage | required, default=first stage |
| priority | Selection | `0`=Low, `1`=Medium, `2`=High, `3`=Critical | default='1' |
| kanban_state | Selection | `normal`, `done`, `blocked` | default='normal' |
| sla_status_ids | One2many(helpdesk.sla.status) | SLA tracking records | |
| sla_deadline | Datetime | Earliest SLA deadline (computed) | compute, store=True |
| sla_reached | Boolean | All SLAs met | compute, store=True |
| sla_failed | Boolean | Any SLA breached | compute, store=True |
| date_created | Datetime | Ticket creation timestamp | default=now, readonly |
| date_assigned | Datetime | When agent was assigned | |
| date_first_response | Datetime | First public reply timestamp | |
| date_resolved | Datetime | When moved to resolved stage | |
| date_closed | Datetime | When moved to closed stage | |
| date_last_stage_update | Datetime | Last stage transition | |
| active | Boolean | Archive flag | default=True |
| tag_ids | Many2many(helpdesk.tag) | Optional tags | |

**Mixins**: `mail.thread`, `mail.activity.mixin`, `portal.mixin`

**State Transitions**:
```text
New → In Progress → Waiting for User → Resolved → Closed
  ↑                                       │         │
  └───────────────────────────────────────┘─────────┘
                  (Reopen)
```

### helpdesk.stage

Configurable workflow stages for the ticket kanban.

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| name | Char | Stage name | required, translate=True |
| sequence | Integer | Display order | default=10 |
| fold | Boolean | Folded in kanban view | default=False |
| is_close | Boolean | Marks ticket as closed | default=False |
| is_done | Boolean | Marks ticket as resolved | default=False |
| description | Text | Stage description | |

**Default data** (noupdate="1"):
1. New (sequence=1)
2. In Progress (sequence=2)
3. Waiting for User (sequence=3, fold=True)
4. Resolved (sequence=4, is_done=True)
5. Closed (sequence=5, is_close=True, fold=True)

### helpdesk.category

Configurable ticket classification linked to team routing.

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| name | Char | Category name | required, translate=True |
| team_id | Many2one(helpdesk.team) | Default team for routing | |
| description | Text | Category description | |
| sequence | Integer | Display order | default=10 |
| active | Boolean | Archive flag | default=True |

**Default data** (noupdate="1"):
1. Hardware
2. Software
3. Network
4. Access/Permissions
5. General

### helpdesk.sla.policy

SLA rules defining response and resolution time targets.

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| name | Char | Policy name | required |
| team_id | Many2one(helpdesk.team) | Team this policy applies to | required |
| priority | Selection | Minimum priority to trigger | `0`/`1`/`2`/`3`, required |
| category_ids | Many2many(helpdesk.category) | Categories (empty = all) | |
| time_response | Float | Response time target (hours) | min=0 |
| time_resolution | Float | Resolution time target (hours) | min=0 |
| stage_id | Many2one(helpdesk.stage) | Target stage to reach | required |
| active | Boolean | Archive flag | default=True |

### helpdesk.sla.status

Per-ticket SLA tracking record (one per applicable SLA policy).

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| ticket_id | Many2one(helpdesk.ticket) | Parent ticket | required, ondelete='cascade' |
| sla_policy_id | Many2one(helpdesk.sla.policy) | SLA policy being tracked | required |
| deadline | Datetime | Computed deadline | compute, store=True |
| reached | Boolean | SLA target met on time | default=False |
| failed | Boolean | SLA target breached | default=False |
| reached_date | Datetime | When SLA was met | |
| exceeded_hours | Float | Hours past deadline (if breached) | compute |

### helpdesk.tag

Optional tags for additional ticket classification.

| Field | Type | Description | Constraints |
|-------|------|-------------|-------------|
| name | Char | Tag name | required, unique |
| color | Integer | Color index | |

## Security Groups

Defined in `security/helpdesk_security.xml`:

| Group | XML ID | Implied By | Access |
|-------|--------|------------|--------|
| Helpdesk User | `group_helpdesk_user` | `base.group_user` | Submit tickets, view own tickets |
| Helpdesk Agent | `group_helpdesk_agent` | `group_helpdesk_user` | Manage assigned/team tickets, reply, reassign |
| Helpdesk Manager | `group_helpdesk_manager` | `group_helpdesk_agent` | Full access: config, SLA, teams, dashboard, all tickets |

## Record Rules

| Rule | Group | Domain |
|------|-------|--------|
| User sees own tickets | `group_helpdesk_user` | `[('partner_id', '=', user.partner_id.id)]` |
| Agent sees team tickets | `group_helpdesk_agent` | `['|', ('user_id', '=', user.id), ('team_id.member_ids', 'in', [user.id])]` |
| Manager sees all | `group_helpdesk_manager` | `[(1, '=', 1)]` |
