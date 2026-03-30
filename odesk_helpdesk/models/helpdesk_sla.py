from odoo import fields, models


class HelpdeskSlaPolicy(models.Model):
    _name = 'helpdesk.sla.policy'
    _description = 'Helpdesk SLA Policy'
    _order = 'name'

    name = fields.Char(required=True)
    team_id = fields.Many2one('helpdesk.team', required=True, string='Team')
    priority = fields.Selection(
        [('0', 'Low'), ('1', 'Medium'), ('2', 'High'), ('3', 'Critical')],
        required=True, default='1', string='Minimum Priority',
    )
    category_ids = fields.Many2many(
        'helpdesk.category', string='Categories',
        help='Leave empty to apply to all categories.',
    )
    time_response = fields.Float(string='Response Time (Hours)')
    time_resolution = fields.Float(string='Resolution Time (Hours)')
    stage_id = fields.Many2one(
        'helpdesk.stage', required=True, string='Target Stage',
    )
    active = fields.Boolean(default=True)
