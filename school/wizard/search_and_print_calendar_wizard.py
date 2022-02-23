from odoo import api, models, fields, _

class SearchAndPrintCalendarWizard(models.TransientModel):
    _name = "school.search.and.print.calendar.wizard"
    _description = "Search and Print Calendar Wizard"

    student_id = fields.Many2one('school.students', string='Student', required=True)
    date_from = fields.Date(string='Date From')
    date_to = fields.Date(string='Date To')

    def school_test_button(self):
        print('test button clicked')
        # try to ignore close popup after clicking this button, but not working
        # return {
        #     "type": "ir.actions.do_nothing"
        # }

    def school_print_calendars(self):
        # combine search condition
        search_conditions = []
        if (self.student_id):
            search_conditions += [('student_id','=',self.student_id.id)]
        if (self.date_from):
            search_conditions += [('date', '>=', self.date_from)]
        if (self.date_to):
            search_conditions += [('date', '<=', self.date_to)]

        calendars_data = self.env['school.calendar'].search_read(search_conditions)
        # pass data to view
        data = {
            'form_data': self.read()[0],
            'calendars_data': calendars_data
        }
        # call report action
        # this action is get from report/calendar_report.xml
        report_action = self.env.ref('school.action_report_calendar').report_action(self, data=data)

        return report_action

    def school_print_calendars_xlsx(self):
        # combine search condition
        search_conditions = []
        if (self.student_id):
            search_conditions += [('student_id','=',self.student_id.id)]
        if (self.date_from):
            search_conditions += [('date', '>=', self.date_from)]
        if (self.date_to):
            search_conditions += [('date', '<=', self.date_to)]

        calendars_data = self.env['school.calendar'].search_read(search_conditions)
        # pass data to view
        data = {
            'form_data': self.read()[0],
            'calendars_data': calendars_data
        }
        # call report action
        # this action is get from report/calendar_report.xml
        report_action = self.env.ref('school.action_report_calendar_xlsx').report_action(self, data=data)

        return report_action