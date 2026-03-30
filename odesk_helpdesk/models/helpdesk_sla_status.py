from datetime import timedelta

from odoo import api, fields, models


class HelpdeskSlaStatus(models.Model):
    _name = 'helpdesk.sla.status'
    _description = 'Helpdesk SLA Status'

    ticket_id = fields.Many2one(
        'helpdesk.ticket', required=True, ondelete='cascade',
    )
    sla_policy_id = fields.Many2one(
        'helpdesk.sla.policy', required=True, string='SLA Policy',
    )
    deadline = fields.Datetime(compute='_compute_deadline', store=True)
    reached = fields.Boolean(default=False)
    failed = fields.Boolean(default=False)
    reached_date = fields.Datetime()
    exceeded_hours = fields.Float(compute='_compute_exceeded_hours')

    @api.depends('ticket_id.date_created', 'sla_policy_id.time_resolution')
    def _compute_deadline(self):
        for status in self:
            if status.ticket_id.date_created and status.sla_policy_id.time_resolution:
                status.deadline = status.ticket_id.date_created + timedelta(
                    hours=status.sla_policy_id.time_resolution,
                )
            else:
                status.deadline = False

    @api.depends('deadline', 'reached', 'reached_date')
    def _compute_exceeded_hours(self):
        now = fields.Datetime.now()
        for status in self:
            if not status.deadline:
                status.exceeded_hours = 0.0
            elif status.reached and status.reached_date:
                if status.reached_date > status.deadline:
                    delta = status.reached_date - status.deadline
                    status.exceeded_hours = delta.total_seconds() / 3600.0
                else:
                    status.exceeded_hours = 0.0
            elif not status.reached and now > status.deadline:
                delta = now - status.deadline
                status.exceeded_hours = delta.total_seconds() / 3600.0
            else:
                status.exceeded_hours = 0.0
