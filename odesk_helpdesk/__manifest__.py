{
    'name': 'IT Helpdesk',
    'version': '18.0.1.0.0',
    'category': 'Services/Helpdesk',
    'summary': 'IT Helpdesk with SLA tracking, auto-assignment, and portal',
    'description': """
IT Helpdesk Plugin for Odoo
===========================
Complete IT helpdesk system with:
- Ticket submission with auto-sequencing and email notifications
- Kanban-based ticket management with configurable stages
- Team-based routing with round-robin auto-assignment
- SLA tracking with escalation notifications
- Management dashboard with graphs and pivot views
- Website portal for ticket submission and tracking
    """,
    'author': 'Định Nguyễn',
    'website': '',
    'license': 'LGPL-3',
    'depends': ['base', 'mail', 'portal', 'web'],
    'data': [
        'security/helpdesk_security.xml',
        'security/ir.model.access.csv',
        'data/helpdesk_sequence_data.xml',
        'data/helpdesk_stage_data.xml',
        'data/helpdesk_category_data.xml',
        'data/helpdesk_mail_template_data.xml',
        'data/helpdesk_cron_data.xml',
        'views/helpdesk_stage_views.xml',
        'views/helpdesk_category_views.xml',
        'views/helpdesk_team_views.xml',
        'views/helpdesk_ticket_views.xml',
        'views/helpdesk_sla_views.xml',
        'views/helpdesk_dashboard_views.xml',
        'views/helpdesk_menus.xml',
        'views/portal_templates.xml',
    ],
    'demo': [
        'demo/helpdesk_demo.xml',
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
