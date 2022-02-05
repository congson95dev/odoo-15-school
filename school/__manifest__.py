{
    'name': "School",
    'version': '1.0',
    'depends': [
        'base',
        'sale',
        'mail'
    ],
    'author': "Fudo",
    'description': """
    This is a custom School module from Fudo
    """,
    # data files always loaded at installation
    'data': [
        'security/ir.model.access.csv',
        'report/student_report.xml',
        'report/student_report_template.xml',
        'wizard/create_calendar_wizard_view.xml',
        'views/students.xml',
        'views/kids.xml',
        'views/genders.xml',
        'views/calendar.xml',
        'views/sale.xml',
        'data/sequence.xml'
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