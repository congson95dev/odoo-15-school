from odoo import api, models, fields, _

class SearchAndPrintCalendarWizard(models.TransientModel):
    _name = "school.search.and.print.calendar.wizard"
    _description = "Search and Print Calendar Wizard"

    student_id = fields.Many2one('school.students', string='Student', required=True)
    date_from = fields.Datetime(string='Date From')
    date_to = fields.Datetime(string='Date To')

    def school_print_calendars(self):
        calendars_data = self.env['school.calendar'].search_read([('student_id','=',self.student_id.id)])
        # pass data to view
        data = {
            'form_data': self.read()[0],
            'calendars_data': calendars_data
        }
        # call report action
        report_action = self.env.ref('school.action_report_calendar').report_action(self, data=data)

        return report_action