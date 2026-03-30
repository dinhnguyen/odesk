# IT Helpdesk for Odoo 18

A complete IT helpdesk module for Odoo 18.0 with ticket management, SLA tracking, team-based routing, and a self-service portal.

## Features

### Ticket Management
- Kanban board with configurable stages (New, In Progress, Waiting, Resolved, Closed)
- Priority levels: Low, Medium, High, Critical
- Auto-generated ticket numbers via sequence
- Email notifications on ticket creation, assignment, and stage changes
- File attachments support
- Full message thread (mail.thread integration)

### Team-Based Routing
- Create multiple support teams with dedicated members and a team leader
- Assign categories to teams for automatic routing
- **Round-robin auto-assignment** — tickets are automatically distributed among team members
- Manual assignment option

### SLA Tracking
- Define SLA policies per team with response and resolution time targets
- Automatic deadline calculation based on ticket creation time
- Real-time SLA status tracking (reached, failed, exceeded hours)
- **Cron-based escalation** — sends warnings when a ticket reaches 80% of its SLA deadline
- SLA compliance reporting per ticket

### Auto-Close
- Configurable auto-close period per team (default: 7 days)
- Resolved tickets are automatically moved to Closed stage after the defined period
- Runs via scheduled cron job

### Management Dashboard
- Graph view: tickets by category
- Pivot view: resolution time by agent and category
- Filterable and groupable by all key fields

### Self-Service Portal
- `/my/helpdesk` — list and search submitted tickets
- `/my/helpdesk/new` — submit a new ticket with category, priority, description, and attachments
- `/my/helpdesk/<id>` — view ticket details, status, and message history
- `/my/helpdesk/<id>/reply` — reply to a ticket with message and attachments
- Portal entry on the "My" homepage with ticket count

## Installation

### Requirements
- Odoo 18.0
- Python 3.10+
- Dependencies: `base`, `mail`, `portal`, `web`

### Steps

1. Copy the `odesk_helpdesk` folder into your Odoo addons directory:

```bash
cp -r odesk_helpdesk /path/to/odoo/addons/
```

2. Restart Odoo and update the apps list:

```bash
python odoo-bin -c odoo.conf -u base
```

3. Install via UI: go to **Apps**, search for "IT Helpdesk", click **Install**.

   Or install via command line:

```bash
python odoo-bin -c odoo.conf -d <your_database> -i odesk_helpdesk
```

## Configuration

After installation, configure in this order:

### 1. Teams
Go to **IT Helpdesk > Configuration > Teams** and create at least one team:
- Set a **Team Leader**
- Add **Members** for ticket assignment
- Choose **Assignment Method**: Manual or Round Robin
- Set **Auto Close Days** (default: 7)

### 2. Categories
Go to **IT Helpdesk > Configuration > Categories** and assign a **Default Team** to each category. This is required for ticket creation from the portal.

Default categories: Hardware, Software, Network, Access/Permissions, General.

### 3. Stages
Go to **IT Helpdesk > Configuration > Stages** to customize the workflow.

Default stages:

| Stage | Sequence | Type |
|-------|----------|------|
| New | 1 | — |
| In Progress | 2 | — |
| Waiting for User | 3 | — |
| Resolved | 4 | Done |
| Closed | 5 | Closing |

### 4. SLA Policies (Optional)
Go to **IT Helpdesk > Configuration > SLA Policies** to define service level agreements:
- **Team** — which team this policy applies to
- **Priority** — minimum priority level to trigger this SLA
- **Categories** — leave empty to apply to all categories
- **Target Stage** — the stage that must be reached within the time limit
- **Response Time / Resolution Time** — time in hours

## Usage

### Backend (Agents & Managers)
- Access tickets via **IT Helpdesk > Tickets**
- Drag tickets between stages on the kanban board
- Click **Assign to Me** to self-assign
- Use **Reopen** to reopen closed/resolved tickets
- View SLA status in the SLA tab on ticket form
- Access dashboard via **IT Helpdesk > Dashboard**

### Portal (End Users)
- Navigate to `http://<your-odoo>/my/helpdesk`
- Click **New Ticket** to submit a support request
- Track ticket status and reply with messages/attachments

## Security Groups

| Group | Access |
|-------|--------|
| Helpdesk User | View own tickets, read-only access to stages/categories/teams |
| Helpdesk Agent | View team tickets, manage assignments, update SLA status |
| Helpdesk Manager | Full access to all tickets, teams, stages, categories, SLA policies, dashboard |
| Portal User | Submit tickets, view own tickets, add replies |

The admin user is automatically added to the Helpdesk Manager group.

## Module Structure

```
odesk_helpdesk/
├── __init__.py
├── __manifest__.py
├── controllers/
│   └── portal.py              # Portal routes
├── data/
│   ├── helpdesk_category_data.xml
│   ├── helpdesk_cron_data.xml
│   ├── helpdesk_mail_template_data.xml
│   ├── helpdesk_sequence_data.xml
│   └── helpdesk_stage_data.xml
├── models/
│   ├── helpdesk_category.py
│   ├── helpdesk_sla.py
│   ├── helpdesk_sla_status.py
│   ├── helpdesk_stage.py
│   ├── helpdesk_tag.py
│   ├── helpdesk_team.py
│   └── helpdesk_ticket.py
├── security/
│   ├── helpdesk_security.xml
│   └── ir.model.access.csv
├── static/
│   └── description/
│       └── icon.png
└── views/
    ├── helpdesk_category_views.xml
    ├── helpdesk_dashboard_views.xml
    ├── helpdesk_menus.xml
    ├── helpdesk_sla_views.xml
    ├── helpdesk_stage_views.xml
    ├── helpdesk_team_views.xml
    ├── helpdesk_ticket_views.xml
    └── portal_templates.xml
```

## License

LGPL-3
