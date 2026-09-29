# Quickstart: ODesk IT Helpdesk

## Prerequisites

- Odoo 18.0 instance (Community or Enterprise)
- Python 3.10+
- PostgreSQL database configured for Odoo

## Installation

1. Clone or copy the `odesk_helpdesk` directory into your Odoo
   addons path:

   ```bash
   cp -r odesk_helpdesk /path/to/odoo/addons/
   ```

2. Update the Odoo module list:

   ```bash
   ./odoo-bin -d your_database -u base --stop-after-init
   ```

3. In the Odoo backend, navigate to **Apps**, search for
   "IT Helpdesk", and click **Install**.

## Initial Configuration

### 1. Set Up a Helpdesk Team

- Navigate to **IT Helpdesk > Configuration > Teams**
- Click **Create**
- Enter team name (e.g., "IT Support")
- Add team members (agents)
- Set assignment method: **Manual** or **Round Robin**
- Set auto-close days (default: 7)
- Save

### 2. Configure Categories

- Navigate to **IT Helpdesk > Configuration > Categories**
- Default categories are pre-installed: Hardware, Software,
  Network, Access/Permissions, General
- Assign each category to a team for routing
- Add or modify categories as needed

### 3. Define SLA Policies (Optional)

- Navigate to **IT Helpdesk > Configuration > SLA Policies**
- Click **Create**
- Set: name, team, minimum priority, target stage, response
  time (hours), and resolution time (hours)
- Example: "Critical Response" — Team: IT Support, Priority:
  Critical, Response Time: 1h, Resolution Time: 4h

### 4. Assign Security Groups

- Navigate to **Settings > Users & Companies > Users**
- For each user, set the IT Helpdesk access level:
  - **Helpdesk User**: Can submit and view own tickets
  - **Helpdesk Agent**: Can manage and resolve team tickets
  - **Helpdesk Manager**: Full access including configuration

## Usage

### Submit a Ticket (Backend)

1. Navigate to **IT Helpdesk > New Ticket**
2. Fill in: Category, Subject, Description, Priority
3. Click **Save** — ticket number is auto-generated
4. Submitter receives a confirmation email

### Submit a Ticket (Portal)

1. Log into the Odoo portal at `/my`
2. Click **My Tickets** > **New Ticket**
3. Fill in the form and submit
4. Track ticket status from the portal

### Manage Tickets (Agent)

1. Navigate to **IT Helpdesk > Tickets**
2. View the kanban board with tickets by stage
3. Click a ticket to assign, reply, or change stage
4. Drag tickets between stages on the kanban board

### View Dashboard (Manager)

1. Navigate to **IT Helpdesk > Dashboard**
2. View: open tickets, tickets by category, average resolution
   time, SLA compliance rate
3. Use filters for date range, category, and team member

## Demo Data

The module includes demo data for evaluation:
- 1 helpdesk team with 3 agents
- 5 categories (default set)
- 5 stages (default set)
- 2 SLA policies
- 10 sample tickets in various stages

Demo data is loaded automatically when installing with
`--demo` flag or when demo data is enabled in the database.

## Troubleshooting

- **Module not visible in Apps**: Run `odoo-bin -u base` to
  refresh the module list
- **Emails not sending**: Verify outgoing mail server in
  **Settings > Technical > Email > Outgoing Mail Servers**
- **Portal not showing tickets**: Ensure the user has portal
  access and a linked `res.partner` record
