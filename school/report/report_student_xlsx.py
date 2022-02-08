from odoo import models
from datetime import datetime

# Download this module:
# https://apps.odoo.com/apps/modules/15.0/report_xlsx/#installation
class StudentXlsx(models.AbstractModel):
    _name = 'report.school.report_student_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    # row is horizontal line, column is the vertical line, each row is equal to 1 record, each column is equal to 1 column in mysql db
    # open excel and check bottom left if you still don't know what is row and column

    def generate_xlsx_report(self, workbook, data, students):
        # add new sheet
        sheet = workbook.add_worksheet('Students')
        # add format
        bold = workbook.add_format({'bold': True})
        # init row and column
        row = 0
        column = 0
        # test
        self.testExcel(sheet, workbook, bold)
        # format width of column
        sheet.set_column('A:A', 12)
        sheet.set_column('B:B', 25)
        sheet.set_column('D:D', 15)
        sheet.set_column('F:F', 15)
        sheet.set_column('G:G', 15)
        sheet.set_column('H:H', 15)
        # add first line
        sheet.write(row, 0, 'Sequence', bold)
        sheet.write(row, 1, 'Name', bold)
        sheet.write(row, 2, 'Age', bold)
        sheet.write(row, 3, 'Day Of Birth', bold)
        sheet.write(row, 4, 'Gender', bold)
        sheet.write(row, 5, 'Blood Group', bold)
        sheet.write(row, 6, 'Calendar Count', bold)
        sheet.write(row, 7, 'Nationality', bold)
        # add column += 1 after create first line
        row += 1
        # loop
        for obj in students:
            # reset column after each record in the loop
            column = 0
            # print data to excel, after that, column += 1
            sheet.write(row, column, obj.sequence)
            column += 1
            sheet.write(row, column, obj.name)
            column += 1
            student_age = self.checkEmpty(obj.student_age)
            sheet.write(row, column, student_age)
            column += 1
            student_dob = str(self.checkEmpty(obj.student_dob))
            sheet.write(row, column, student_dob)
            column += 1
            student_gender = self.checkEmpty(obj.student_gender)
            sheet.write(row, column, student_gender)
            column += 1
            student_blood_group = self.checkEmpty(obj.student_blood_group)
            sheet.write(row, column, student_blood_group)
            column += 1
            student_calendar_count = self.checkEmpty(obj.student_calendar_count)
            sheet.write(row, column, student_calendar_count)
            column += 1
            nationality = self.checkEmpty(obj.nationality.name)
            sheet.write(row, column, nationality)
            column += 1
            # add column += 1 after create new line
            row += 1

    # check if empty variable, then return "N/A"
    def checkEmpty(self, variable):
        if (variable):
            return variable
        else:
            return "N/A"

    def testExcel(self, sheet, workbook, bold):
        # merge 2 column as one (for testing purpose)
        row_merge = 0
        column_merge = 10
        sheet.merge_range(row_merge, column_merge, row_merge, column_merge + 2, 'Merge Column', bold)

        sheet.set_column('N:N', 20)
        # add new format with style background color = yellow
        yellow = workbook.add_format({'bold': True, 'align': 'center', 'bg_color': 'yellow'})
        sheet.write(row_merge, column_merge + 3, 'Change Format Column', yellow)