from odoo import fields, models


class HelpdeskTeam(models.Model):
    _name = 'helpdesk.team'
    _description = 'Helpdesk Team'
    _order = 'name'

    name = fields.Char(required=True)
    description = fields.Text()
    member_ids = fields.Many2many('res.users', string='Members')
    leader_id = fields.Many2one('res.users', string='Team Leader')
    assignment_method = fields.Selection(
        [('manual', 'Manual'), ('round_robin', 'Round Robin')],
        required=True,
        default='manual',
    )
    category_ids = fields.One2many(
        'helpdesk.category', 'team_id', string='Categories',
    )
    sla_policy_ids = fields.One2many(
        'helpdesk.sla.policy', 'team_id', string='SLA Policies',
    )
    ticket_ids = fields.One2many(
        'helpdesk.ticket', 'team_id', string='Tickets',
    )
    auto_close_days = fields.Integer(default=7, string='Auto-Close After (Days)')
    color = fields.Integer()
    active = fields.Boolean(default=True)

    def _assign_ticket_round_robin(self, ticket):
        self.ensure_one()
        members = self.member_ids
        if not members:
            return
        last_assigned = self.env['helpdesk.ticket'].search([
            ('team_id', '=', self.id),
            ('user_id', 'in', members.ids),
            ('user_id', '!=', False),
        ], order='date_assigned desc, id desc', limit=1)
        if last_assigned and last_assigned.user_id in members:
            member_list = list(members)
            idx = next(
                (i for i, m in enumerate(member_list) if m == last_assigned.user_id),
                -1,
            )
            next_agent = member_list[(idx + 1) % len(member_list)]
        else:
            next_agent = members[0]
        ticket.write({
            'user_id': next_agent.id,
            'date_assigned': fields.Datetime.now(),
        })
