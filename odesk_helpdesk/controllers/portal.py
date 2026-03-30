from odoo import http
from odoo.exceptions import AccessError
from odoo.http import request

from odoo.addons.portal.controllers.portal import CustomerPortal, pager as portal_pager


class HelpdeskPortal(CustomerPortal):

    def _prepare_home_portal_values(self, counters):
        values = super()._prepare_home_portal_values(counters)
        if 'ticket_count' in counters:
            values['ticket_count'] = request.env['helpdesk.ticket'].search_count(
                self._get_ticket_domain()
            )
        return values

    def _get_ticket_domain(self):
        return [('partner_id', '=', request.env.user.partner_id.id)]

    @http.route(
        ['/my/helpdesk', '/my/helpdesk/page/<int:page>'],
        type='http', auth='user', website=True,
    )
    def portal_my_tickets(self, page=1, sortby=None, search=None, search_in='all', **kw):
        domain = self._get_ticket_domain()
        searchbar_sortings = {
            'date': {'label': 'Newest', 'order': 'date_created desc'},
            'name': {'label': 'Subject', 'order': 'name asc'},
            'stage': {'label': 'Stage', 'order': 'stage_id asc'},
            'priority': {'label': 'Priority', 'order': 'priority desc'},
        }
        if not sortby:
            sortby = 'date'
        order = searchbar_sortings[sortby]['order']

        if search and search_in:
            if search_in == 'name':
                domain += [('name', 'ilike', search)]
            elif search_in == 'number':
                domain += [('number', 'ilike', search)]
            else:
                domain += [
                    '|',
                    ('name', 'ilike', search),
                    ('number', 'ilike', search),
                ]

        ticket_count = request.env['helpdesk.ticket'].search_count(domain)
        pager = portal_pager(
            url='/my/helpdesk',
            url_args={'sortby': sortby, 'search': search, 'search_in': search_in},
            total=ticket_count,
            page=page,
            step=10,
        )
        tickets = request.env['helpdesk.ticket'].search(
            domain, order=order, limit=10, offset=pager['offset'],
        )
        values = {
            'tickets': tickets,
            'page_name': 'helpdesk',
            'default_url': '/my/helpdesk',
            'pager': pager,
            'sortby': sortby,
            'searchbar_sortings': searchbar_sortings,
            'search': search,
            'search_in': search_in,
        }
        return request.render('odesk_helpdesk.portal_my_tickets', values)

    @http.route(
        '/my/helpdesk/<int:ticket_id>',
        type='http', auth='user', website=True,
    )
    def portal_my_ticket(self, ticket_id, **kw):
        ticket = request.env['helpdesk.ticket'].browse(ticket_id)
        if not ticket.exists() or ticket.partner_id != request.env.user.partner_id:
            raise AccessError("You do not have access to this ticket.")
        values = {
            'ticket': ticket,
            'page_name': 'helpdesk',
            'success': kw.get('success'),
        }
        return request.render('odesk_helpdesk.portal_my_ticket_detail', values)

    @http.route(
        '/my/helpdesk/new',
        type='http', auth='user', website=True, methods=['GET'],
    )
    def portal_new_ticket(self, **kw):
        categories = request.env['helpdesk.category'].search([])
        values = {
            'categories': categories,
            'page_name': 'helpdesk',
        }
        return request.render('odesk_helpdesk.portal_new_ticket', values)

    @http.route(
        '/my/helpdesk/new',
        type='http', auth='user', website=True, methods=['POST'],
        csrf=True,
    )
    def portal_submit_ticket(self, **post):
        category = request.env['helpdesk.category'].browse(int(post.get('category_id', 0)))
        if not category.exists():
            return request.redirect('/my/helpdesk/new')
        if not category.team_id:
            return request.render('odesk_helpdesk.portal_new_ticket', {
                'categories': request.env['helpdesk.category'].search([]),
                'page_name': 'helpdesk',
                'error': 'The selected category has no team assigned. Please contact the administrator or choose another category.',
            })
        vals = {
            'name': post.get('subject', '')[:200],
            'description': post.get('description', ''),
            'category_id': category.id,
            'priority': post.get('priority', '1'),
            'partner_id': request.env.user.partner_id.id,
            'team_id': category.team_id.id,
        }
        try:
            ticket = request.env['helpdesk.ticket'].sudo().create(vals)
        except Exception as e:
            return request.render('odesk_helpdesk.portal_new_ticket', {
                'categories': request.env['helpdesk.category'].search([]),
                'page_name': 'helpdesk',
                'error': 'Failed to create ticket: %s' % str(e),
            })
        attachments = request.httprequest.files.getlist('attachment')
        for attachment in attachments:
            if attachment.filename:
                request.env['ir.attachment'].sudo().create({
                    'name': attachment.filename,
                    'datas': attachment.read(),
                    'res_model': 'helpdesk.ticket',
                    'res_id': ticket.id,
                })
        return request.redirect('/my/helpdesk/%s?success=1' % ticket.id)

    @http.route(
        '/my/helpdesk/<int:ticket_id>/reply',
        type='http', auth='user', website=True, methods=['POST'],
        csrf=True,
    )
    def portal_ticket_reply(self, ticket_id, **post):
        ticket = request.env['helpdesk.ticket'].browse(ticket_id)
        if not ticket.exists() or ticket.partner_id != request.env.user.partner_id:
            raise AccessError("You do not have access to this ticket.")
        message = post.get('message', '').strip()
        if message:
            ticket.sudo().message_post(
                body=message,
                message_type='comment',
                subtype_xmlid='mail.mt_comment',
                author_id=request.env.user.partner_id.id,
            )
        attachments = request.httprequest.files.getlist('attachment')
        for attachment in attachments:
            if attachment.filename:
                request.env['ir.attachment'].sudo().create({
                    'name': attachment.filename,
                    'datas': attachment.read(),
                    'res_model': 'helpdesk.ticket',
                    'res_id': ticket.id,
                })
        return request.redirect('/my/helpdesk/%s' % ticket_id)
