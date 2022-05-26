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
        # data to import should be right below security
        'data/data.xml',
        # import by csv
        # the name of the csv file is model name
        # inside that file, first column must be id of the record (name it anything you like)
        # after the first column, you can fill any column in that model
        'data/school.students.csv',
        # data to import should be right above the others
        'report/student_report.xml',
        'report/student_report_template.xml',
        'report/calendar_report.xml',
        'report/calendar_report_template.xml',
        'report/sale_report_templates_inherit.xml',
        'wizard/create_calendar_wizard_view.xml',
        'wizard/search_and_print_calendar_wizard_view.xml',
        'views/students.xml',
        'views/teachers.xml',
        'views/kids.xml',
        'views/genders.xml',
        'views/calendar.xml',
        'views/sale.xml',
        'views/function.xml',
        'views/students_template.xml',
        'views/settings.xml',
        'data/sequence.xml',
        'data/cron.xml',
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