# Portal Routes Contract: IT Helpdesk

**Date**: 2026-03-30

## Website Portal Routes

These routes are exposed via the `portal` module for authenticated
portal users.

### GET /my/helpdesk

**Description**: List all tickets submitted by the current portal user.

**Access**: Authenticated portal user (`portal.group_portal`)

**Parameters**:
- `page` (int, optional): Page number for pagination, default=1
- `sortby` (str, optional): Sort field (`date`, `name`, `stage`, `priority`), default=`date`
- `search` (str, optional): Search in ticket subject
- `search_in` (str, optional): Search scope (`name`, `number`, `all`), default=`all`

**Response**: QWeb rendered page with paginated ticket list showing
number, subject, stage, priority, creation date, and last update.

---

### GET /my/helpdesk/\<int:ticket_id\>

**Description**: View a single ticket's details and conversation.

**Access**: Authenticated portal user, must be the ticket submitter
(`partner_id == request.env.user.partner_id`)

**Parameters**:
- `ticket_id` (int, required): Ticket database ID

**Response**: QWeb rendered page with ticket details (all fields),
chatter messages, and a reply form.

**Error**: 403 if user is not the ticket submitter.

---

### GET /my/helpdesk/new

**Description**: Display the new ticket submission form.

**Access**: Authenticated portal user

**Response**: QWeb rendered form with fields: category (select),
subject (text), description (textarea), priority (select),
attachments (file upload).

---

### POST /my/helpdesk/new

**Description**: Submit a new ticket from the portal.

**Access**: Authenticated portal user

**Parameters** (form data):
- `category_id` (int, required): Ticket category ID
- `subject` (str, required): Ticket subject, max 200 chars
- `description` (str, required): Ticket description
- `priority` (str, optional): `0`/`1`/`2`/`3`, default=`1`
- `attachment` (file, optional): File attachment(s)

**Response**: Redirect to `/my/helpdesk/<ticket_id>` on success.

**Validation**:
- `category_id` must reference a valid `helpdesk.category`
- `subject` must not be empty
- `description` must not be empty

---

### POST /my/helpdesk/\<int:ticket_id\>/reply

**Description**: Add a reply message to an existing ticket.

**Access**: Authenticated portal user, must be the ticket submitter

**Parameters** (form data):
- `message` (str, required): Reply message body
- `attachment` (file, optional): File attachment(s)

**Response**: Redirect back to `/my/helpdesk/<ticket_id>`.

---

## Email Aliases

| Alias | Action |
|-------|--------|
| Reply to ticket notification | Creates `mail.message` on ticket via `mail.thread` |
| (No catchall alias for v1) | Ticket creation via email alias deferred to v2 |
