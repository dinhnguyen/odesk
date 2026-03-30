from odoo import fields, models


class HelpdeskCategory(models.Model):
    _name = 'helpdesk.category'
    _description = 'Helpdesk Category'
    _order = 'sequence, id'

    name = fields.Char(required=True, translate=True)
    team_id = fields.Many2one('helpdesk.team', string='Default Team')
    description = fields.Text()
    sequence = fields.Integer(default=10)
    active = fields.Boolean(default=True)
