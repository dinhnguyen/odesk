from odoo import fields, models


class HelpdeskTag(models.Model):
    _name = 'helpdesk.tag'
    _description = 'Helpdesk Tag'
    _order = 'name'
    _sql_constraints = [
        ('name_uniq', 'unique (name)', 'Tag name already exists!'),
    ]

    name = fields.Char(required=True)
    color = fields.Integer()
