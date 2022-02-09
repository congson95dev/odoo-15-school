from odoo import api, models, fields, _

class SearchAndPrintCalendarWizard(models.TransientModel):
    _name = "school.search.and.print.calendar.wizard"
    _description = "Search and Print Calendar Wizard"

    student_id = fields.Many2one('school.students', string='Student', required=True)
    date_from = fields.Datetime(string='Date From')
    date_to = fields.Datetime(string='Date To')

    def school_print_calendars(self):
        # Not working
        # Try to create a report from a wizard, but it's not working
        # https://stackoverflow.com/questions/71047099/create-report-from-wizard-in-odoo-15
        data = {
            'form': self.read()[0]
        }
        report_action = self.env.ref('school.action_report_calendar').report_action(self, data=data)

        return report_action