from odoo import api, fields, models


class HelpdeskTicket(models.Model):
    _name = 'helpdesk.ticket'
    _description = 'Helpdesk Ticket'
    _inherit = ['mail.thread', 'mail.activity.mixin', 'portal.mixin']
    _order = 'priority desc, date_created desc, id desc'

    name = fields.Char(string='Subject', required=True, tracking=True)
    number = fields.Char(string='Ticket Number', readonly=True, copy=False)
    description = fields.Html()
    partner_id = fields.Many2one(
        'res.partner', string='Submitter', required=True,
        default=lambda self: self.env.user.partner_id, tracking=True,
    )
    user_id = fields.Many2one(
        'res.users', string='Assigned Agent', tracking=True,
    )
    team_id = fields.Many2one(
        'helpdesk.team', string='Team', required=True, tracking=True,
    )
    category_id = fields.Many2one(
        'helpdesk.category', string='Category', required=True, tracking=True,
    )
    stage_id = fields.Many2one(
        'helpdesk.stage', string='Stage', required=True, tracking=True,
        group_expand='_read_group_stage_ids',
        default=lambda self: self.env['helpdesk.stage'].search([], limit=1, order='sequence'),
    )
    priority = fields.Selection(
        [('0', 'Low'), ('1', 'Medium'), ('2', 'High'), ('3', 'Critical')],
        default='1', tracking=True,
    )
    kanban_state = fields.Selection(
        [('normal', 'In Progress'), ('done', 'Ready'), ('blocked', 'Blocked')],
        default='normal',
    )
    tag_ids = fields.Many2many('helpdesk.tag', string='Tags')

    sla_status_ids = fields.One2many(
        'helpdesk.sla.status', 'ticket_id', string='SLA Status',
    )
    sla_deadline = fields.Datetime(
        string='SLA Deadline', compute='_compute_sla_deadline', store=True,
    )
    sla_reached = fields.Boolean(
        compute='_compute_sla_reached', store=True,
    )
    sla_failed = fields.Boolean(
        compute='_compute_sla_failed', store=True,
    )

    date_created = fields.Datetime(
        string='Created On', default=fields.Datetime.now, readonly=True,
    )
    date_assigned = fields.Datetime(string='Assigned On')
    date_first_response = fields.Datetime(string='First Response')
    date_resolved = fields.Datetime(string='Resolved On')
    date_closed = fields.Datetime(string='Closed On')
    date_last_stage_update = fields.Datetime(string='Last Stage Update')

    resolution_hours = fields.Float(
        string='Resolution Time (Hours)',
        compute='_compute_resolution_hours', store=True,
    )
    is_sla_compliant = fields.Boolean(
        string='SLA Compliant',
        compute='_compute_is_sla_compliant', store=True,
    )

    is_close = fields.Boolean(related='stage_id.is_close')
    is_done = fields.Boolean(related='stage_id.is_done')
    active = fields.Boolean(default=True)

    @api.model
    def _read_group_stage_ids(self, stages, domain):
        return self.env['helpdesk.stage'].search([], order='sequence')

    @api.depends('sla_status_ids.deadline')
    def _compute_sla_deadline(self):
        for ticket in self:
            deadlines = ticket.sla_status_ids.filtered(
                lambda s: s.deadline and not s.reached
            ).mapped('deadline')
            ticket.sla_deadline = min(deadlines) if deadlines else False

    @api.depends('sla_status_ids.reached')
    def _compute_sla_reached(self):
        for ticket in self:
            statuses = ticket.sla_status_ids
            ticket.sla_reached = bool(statuses) and all(s.reached for s in statuses)

    @api.depends('sla_status_ids.failed')
    def _compute_sla_failed(self):
        for ticket in self:
            ticket.sla_failed = any(s.failed for s in ticket.sla_status_ids)

    @api.depends('date_created', 'date_resolved')
    def _compute_resolution_hours(self):
        for ticket in self:
            if ticket.date_created and ticket.date_resolved:
                delta = ticket.date_resolved - ticket.date_created
                ticket.resolution_hours = delta.total_seconds() / 3600.0
            else:
                ticket.resolution_hours = 0.0

    @api.depends('sla_status_ids.reached', 'sla_status_ids.failed')
    def _compute_is_sla_compliant(self):
        for ticket in self:
            statuses = ticket.sla_status_ids
            ticket.is_sla_compliant = bool(statuses) and all(
                s.reached and not s.failed for s in statuses
            )

    @api.model_create_multi
    def create(self, vals_list):
        for vals in vals_list:
            if not vals.get('number'):
                vals['number'] = self.env['ir.sequence'].next_by_code('helpdesk.ticket') or '/'
            if vals.get('category_id') and not vals.get('team_id'):
                category = self.env['helpdesk.category'].browse(vals['category_id'])
                if category.team_id:
                    vals['team_id'] = category.team_id.id
        tickets = super().create(vals_list)
        for ticket in tickets:
            ticket._apply_sla_policies()
            if ticket.team_id.assignment_method == 'round_robin' and not ticket.user_id:
                ticket.team_id._assign_ticket_round_robin(ticket)
        return tickets

    def write(self, vals):
        stage_changed = 'stage_id' in vals
        old_stages = {t.id: t.stage_id for t in self} if stage_changed else {}
        result = super().write(vals)
        if 'user_id' in vals and vals['user_id']:
            for ticket in self:
                if not ticket.date_assigned:
                    ticket.date_assigned = fields.Datetime.now()
        if stage_changed:
            now = fields.Datetime.now()
            new_stage = self.env['helpdesk.stage'].browse(vals['stage_id'])
            for ticket in self:
                ticket.date_last_stage_update = now
                if new_stage.is_done and not ticket.date_resolved:
                    ticket.date_resolved = now
                if new_stage.is_close and not ticket.date_closed:
                    ticket.date_closed = now
            self._update_sla_on_stage_change(new_stage)
        if any(f in vals for f in ('team_id', 'priority', 'category_id')):
            for ticket in self:
                ticket._apply_sla_policies()
        return result

    def action_reopen(self):
        in_progress = self.env['helpdesk.stage'].search(
            [('sequence', '=', 2)], limit=1,
        ) or self.env['helpdesk.stage'].search([], limit=1, order='sequence')
        for ticket in self:
            ticket.write({
                'stage_id': in_progress.id,
                'date_resolved': False,
                'date_closed': False,
            })
            ticket.sla_status_ids.write({'reached': False, 'failed': False, 'reached_date': False})
            ticket.message_post(body="Ticket reopened.")

    def action_assign_to_me(self):
        self.write({'user_id': self.env.uid})

    def _apply_sla_policies(self):
        for ticket in self:
            if not ticket.team_id:
                continue
            policies = self.env['helpdesk.sla.policy'].search([
                ('team_id', '=', ticket.team_id.id),
                ('priority', '<=', ticket.priority),
                ('active', '=', True),
                '|',
                ('category_ids', '=', False),
                ('category_ids', 'in', ticket.category_id.ids),
            ])
            existing_policy_ids = ticket.sla_status_ids.mapped('sla_policy_id').ids
            for policy in policies:
                if policy.id not in existing_policy_ids:
                    self.env['helpdesk.sla.status'].create({
                        'ticket_id': ticket.id,
                        'sla_policy_id': policy.id,
                    })

    def _update_sla_on_stage_change(self, new_stage):
        now = fields.Datetime.now()
        for ticket in self:
            for status in ticket.sla_status_ids:
                if status.reached:
                    continue
                if status.sla_policy_id.stage_id == new_stage:
                    status.reached = True
                    status.reached_date = now
                    if status.deadline and now > status.deadline:
                        status.failed = True
                    else:
                        status.failed = False

    def _cron_auto_close_tickets(self):
        teams = self.env['helpdesk.team'].search([('auto_close_days', '>', 0)])
        resolved_stages = self.env['helpdesk.stage'].search([('is_done', '=', True)])
        close_stage = self.env['helpdesk.stage'].search([('is_close', '=', True)], limit=1)
        if not close_stage:
            return
        for team in teams:
            threshold = fields.Datetime.subtract(
                fields.Datetime.now(), days=team.auto_close_days,
            )
            tickets = self.search([
                ('team_id', '=', team.id),
                ('stage_id', 'in', resolved_stages.ids),
                ('date_last_stage_update', '<=', threshold),
            ])
            if tickets:
                tickets.write({'stage_id': close_stage.id})

    def _cron_sla_escalation(self):
        now = fields.Datetime.now()
        open_stages = self.env['helpdesk.stage'].search([
            ('is_done', '=', False), ('is_close', '=', False),
        ])
        tickets = self.search([
            ('stage_id', 'in', open_stages.ids),
            ('sla_deadline', '!=', False),
            ('sla_failed', '=', False),
        ])
        for ticket in tickets:
            if not ticket.sla_deadline:
                continue
            total = (ticket.sla_deadline - ticket.date_created).total_seconds()
            elapsed = (now - ticket.date_created).total_seconds()
            if total > 0 and elapsed / total >= 0.8:
                ticket.message_post(
                    body="SLA Warning: This ticket is approaching its SLA deadline.",
                    subject="SLA Escalation Warning",
                    partner_ids=(
                        (ticket.user_id.partner_id | ticket.team_id.leader_id.partner_id)
                        .filtered(lambda p: p).ids
                    ),
                    message_type='notification',
                    subtype_xmlid='mail.mt_note',
                )

    def _compute_access_url(self):
        super()._compute_access_url()
        for ticket in self:
            ticket.access_url = '/my/helpdesk/%s' % ticket.id
