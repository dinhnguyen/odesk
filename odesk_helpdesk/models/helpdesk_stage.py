from odoo import fields, models


class HelpdeskStage(models.Model):
    _name = 'helpdesk.stage'
    _description = 'Helpdesk Stage'
    _order = 'sequence, id'

    name = fields.Char(required=True, translate=True)
    sequence = fields.Integer(default=10)
    fold = fields.Boolean(string='Folded in Kanban')
    is_close = fields.Boolean(string='Closing Stage')
    is_done = fields.Boolean(string='Resolved Stage')
    description = fields.Text()
