from odoo import api, models, fields

# in report, this file is not neccessary
# this file is used for override variables of report

class StudentReport(models.Model):
    # this _name should be template id in view file report/student_report_template.xml
    # so we will override variable of view which have id = report_student
    _name = "report.school.report_student"
    _description = "Student Report"

    # this _get_report_values is default function, which used to override variables in report
    @api.model
    def _get_report_values(self, docids, data=None):
        # browse equal to search([('id','=',docids)])
        docs = self.env['school.students'].browse(docids)

        # we can also return some other variables and call in the view
        return {
            'docs': docs,
        }
