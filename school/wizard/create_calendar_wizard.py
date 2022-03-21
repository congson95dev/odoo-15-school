from odoo import api, models, fields, _

class CreateCalendarWizard(models.TransientModel):
    _name = "school.create.calendar.wizard"
    _description = "Create Calendar Wizard"

    sequence = fields.Char(string='Sequence', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'))
    student_id = fields.Many2one('school.students', string='Student', required=True)
    teacher_id = fields.Many2one('school.teachers', string='Teachers', required=True)
    student_age = fields.Integer(string='Age', related='student_id.student_age')
    student_gender = fields.Selection([('m', 'Male'), ('f', 'Female'), ('o', 'Other')], string='Gender', related='student_id.student_gender')
    date = fields.Datetime(string='Date')

    # create new calendar when click save button
    def school_create_calendar(self):
        # set values dictionary
        vals = {
            'sequence': self.sequence,
            'student_id': self.student_id.id,
            'teacher_id': self.teacher_id.id,
            'student_age': self.student_age,
            'student_gender': self.student_gender,
            'date': self.date
        }
        # save to db
        calendar = self.env['school.calendar'].create(vals)
        # get id
        calendar_id = calendar.id
        # load form by id of create calendar
        return {
            'name': 'Calendar',
            'view_mode': 'form',
            'res_model': 'school.calendar',
            'type': 'ir.actions.act_window',
            # 'target': 'new' # Add this if you need the form loaded is a popup
            # 'form_view_initial_mode': 'edit' is to show edit form mode after create calendar by popup, normally, it show view form mode.
            'context': {'form_view_initial_mode': 'edit'},
            'res_id': calendar_id
        }

    # view list calendars based on student id
    def school_view_calendars(self):
        # get id
        student_id = self.student_id.id
        # load form by id
        return {
            'name': 'Calendars',
            'view_mode': 'tree,form',
            'res_model': 'school.calendar',
            'type': 'ir.actions.act_window',
            # 'target': 'new' # Add this if you need the form loaded is a popup
            'domain': [('student_id','=',student_id)]
        }

    # override function create
    @api.model
    def create(self, vals):
        # show sequence
        if vals.get('sequence', _('New')) == _('New'):
            # the name inside next_by_code is get by file data/sequence.xml
            vals['sequence'] = self.env['ir.sequence'].next_by_code('school.calendar') or _('New')

        res = super(CreateCalendarWizard, self).create(vals)
        return res

    # set default value for popup by current student or teacher
    @api.model
    def default_get(self, fields_list):
        res = super(CreateCalendarWizard, self).default_get(fields_list)
        # get id by self._context
        active_id = self._context.get('active_id')
        active_model = self.env.context.get('active_model')
        if (active_model == 'school.students'):
            # if current model is school.students, then load student data by current student
            # load by id
            student = self.env['school.students'].search([('id','=',active_id)])
            # add data
            res['student_id'] = student.id
            res['student_age'] = student.student_age
            res['student_gender'] = student.student_gender
        elif (active_model == 'school.teachers'):
            # if current model is school.teachers, then load teacher data by current teacher
            # load by id
            teacher = self.env['school.teachers'].search([('id', '=', active_id)])
            # add data
            res['teacher_id'] = teacher.id

        return res