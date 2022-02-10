from odoo import models
from datetime import datetime

# Download this module:
# https://apps.odoo.com/apps/modules/15.0/report_xlsx/#installation
class CalendarXlsx(models.AbstractModel):
    _name = 'report.school.report_calendar_xlsx'
    _inherit = 'report.report_xlsx.abstract'

    # row is horizontal line, column is the vertical line, each row is equal to 1 record, each column is equal to 1 column in mysql db
    # open excel and check bottom left if you still don't know what is row and column

    # when create report xlsx by wizard, it will print all the data in variable "data" below
    # so we need to use data.get('something') to get variable we want

    def generate_xlsx_report(self, workbook, data, calendars):
        # add new sheet
        sheet = workbook.add_worksheet('Calendars')
        # add format
        bold = workbook.add_format({'bold': True})
        # init row and column
        row = 0
        column = 0
        # format width of column
        sheet.set_column('A:A', 12)
        sheet.set_column('B:B', 25)
        # add first line
        sheet.write(row, 0, 'Sequence', bold)
        sheet.write(row, 1, 'Date', bold)
        sheet.write(row, 2, 'State', bold)
        # add column += 1 after create first line
        row += 1
        # when create report xlsx by wizard, it will print all the data in variable "data" below
        # so we need to use data.get('something') to get variable we want
        calendars_data = data.get('calendars_data')
        # loop
        for obj in calendars_data:
            # reset column after each record in the loop
            column = 0
            # print data to excel, after that, column += 1
            sequence = self.checkEmpty(obj.get('sequence'))
            sheet.write(row, column, sequence)
            column += 1
            date = str(self.checkEmpty(obj.get('date')))
            sheet.write(row, column, date)
            column += 1
            state = self.checkEmpty(obj.get('state'))
            sheet.write(row, column, state)
            column += 1
            # add column += 1 after create new line
            row += 1

    # check if empty variable, then return "N/A"
    def checkEmpty(self, variable):
        if (variable):
            return variable
        else:
            return "N/A"