{
    'name': "School",
    'version': '1.0',
    'depends': [
        'base',
        'sale',
        'mail',
        'report_xlsx'
    ],
    'author': "Fudo",
    'description': """
    This is a custom School module from Fudo
    """,
    # data files always loaded at installation
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'report/student_report.xml',
        'report/student_report_template.xml',
        'report/calendar_report.xml',
        'report/calendar_report_template.xml',
        'wizard/create_calendar_wizard_view.xml',
        'wizard/search_and_print_calendar_wizard_view.xml',
        'views/students.xml',
        'views/teachers.xml',
        'views/kids.xml',
        'views/genders.xml',
        'views/calendar.xml',
        'views/sale.xml',
        'views/function.xml',
        'data/sequence.xml',
        'data/data.xml',
        'data/mail_template_data.xml',
    ],
    # data files containing optionally loaded demonstration data
    # 'demo': [
    #     'demo/school_demo_data.xml',
    # ],
    'license': 'LGPL-3',
    'installable': True,
    'application': True,
    'auto_install': True
}