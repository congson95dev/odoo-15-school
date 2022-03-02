from odoo import api, models, fields, _
from odoo.exceptions import ValidationError
from datetime import datetime
import pytz

class Students(models.Model):
    _name = "school.students"
    _description = "Students"

    # when you inherit other modules, you must add it in depends in __manifest__.py
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # call to system configuration
    # have to define the function before we call it
    def _get_default_age(self):
        return self.env['ir.config_parameter'].sudo().get_param('school.school_student_default_age')

    # tracking=True is track whenever you change the data of record
    # it will make a note that show what has been changed in chatbox in bottom of the edit form view
    # but you will need to make a chatbox so this tracking note can be show

    # copy = False is to ignore from copy() function
    # when you add this copy = False, the attribute won't be copy when you click dupplicate

    # this field is for sequence id
    sequence = fields.Char(string='Sequence', required=True, copy=False, readonly=True,
                       states={'draft': [('readonly', False)]}, index=True, default=lambda self: _('New'), tracking=True)
    name = fields.Char(string='Name', tracking=True)
    middle_name = fields.Char(string='Middle Name', required=True, tracking=True)
    last_name = fields.Char(string='Last Name', required=True, tracking=True)
    email = fields.Char(string='Email', required=False, tracking=True)
    photo = fields.Binary(string='Photo', tracking=True)
    # default=_get_default_age is set default by a function, and that function call to system configuration param which we set earlier
    student_age = fields.Integer(string='Age', tracking=True, copy=False, default=_get_default_age)
    student_dob = fields.Date(string="Date of Birth", tracking=True)
    student_gender = fields.Selection([('m', 'Male'), ('f', 'Female'), ('o', 'Other')], string='Gender', tracking=True)
    student_blood_group = fields.Selection(
        [('A+', 'A+ve'), ('B+', 'B+ve'), ('O+', 'O+ve'), ('AB+', 'AB+ve'),
         ('A-', 'A-ve'), ('B-', 'B-ve'), ('O-', 'O-ve'), ('AB-', 'AB-ve')],
        string='Blood Group', tracking=True)
    # add store=True will make compute function not working anymore, don't know how to fix it yet, i've removed it for now
    student_calendar_count = fields.Integer(string="Calendar Count", compute="_compute_student_calendar_count", tracking=True)
    nationality = fields.Many2one('res.country', string='Nationality', tracking=True)
    calendar_ids = fields.One2many('school.calendar', 'student_id', string="Calendars")
    # show archive / unarchive in list
    active = fields.Boolean(string="Active", default=True)


    # compute function
    def _compute_student_calendar_count(self):
        # count student_calendar_count
        for record in self:
            student_calendar_count = self.env['school.calendar'].search_count([('student_id','=',record.id)])
            record.student_calendar_count = student_calendar_count

    # override function create
    @api.model
    def create(self, vals):
        # show sequence
        if vals.get('sequence', _('New')) == _('New'):
            # the name inside next_by_code is get by file data/sequence.xml
            vals['sequence'] = self.env['ir.sequence'].next_by_code('school.students') or _('New')

        # if not get data from field "name", we will add it by middle_name + last_name
        if not vals.get('name'):
            vals['name'] = vals['middle_name'] + " " + vals['last_name']
        res = super(Students, self).create(vals)
        return res

    # override function write (write = update)
    def write(self, vals):
        print('successfully override write function')
        res = super(Students, self).write(vals)
        return res

    # override function copy
    def copy(self, default=None):
        self.ensure_one()
        default = dict(default or {})
        if 'name' not in default:
            # add (copy) after name
            default['name'] = _("%s (copy)") % (self.name)
        return super(Students, self).copy(default=default)

    # override function name_get
    # this function work when we click on dropdown which listed the records of this model
    # Ex: create new calendar -> click on students dropdown
    def name_get(self):
        result = []
        for record in self:
            # add sequence before name
            # Ex: [S00001] student 1
            name = '[' + record.sequence + '] ' + record.name
            result.append((record.id, name))
        return result

    @api.constrains('name')
    def check_name(self):
        # check if name exists in db, then throw error
        for record in self:
            # we need the ('id','!=',record.id) because we need to remove current record from the constrain
            # or else, it will always found the record
            # this only happen in contrains
            student = self.env['school.students'].search([('name','=',record.name),('id','!=',record.id)])
            if (student):
                raise ValidationError(_('Name %s already exists', self.name))

    # example of redirect
    def redirect_to_github(self):
        return {
            'type': 'ir.actions.act_url',
            'target': 'new',
            'url': 'https://github.com/saxsax1995/odoo-15-school',
        }

    # smart button action
    def action_open_calendar(self):
        # redirect to calendar page
        return {
            'name': 'Calendars',
            # add view_type to this action will have issue: No view found for act_window action undefined
            # 'view_type': 'tree',
            'view_mode': 'tree,form',
            'res_model': 'school.calendar',
            'type': 'ir.actions.act_window',
            'target': 'current',
            'domain': [('student_id', '=', self.id)],
            # this will pass default student_id to the form view when you click "Create" button after go to list view by Smart Button
            # so when you click "Create" button, the form will auto filled all the student data for you
            # syntax: default_{some_field}
            'context': {'default_student_id': self.id},
        }

    def run_function_directly(self):
        print('successfully run function')

        # convert datetime variable to user timezone
        # (not working because issue ValueError: <class 'AttributeError'>: "'str' object has no attribute 'tzinfo'" while evaluating)
        # i guess we need a variable to be datetime format before running this convert code

        # original_date = '2006-10-25 14:30:59'
        # user_tz = pytz.timezone(self.env.context.get('tz') or self.env.user.tz)
        # converted_date = pytz.utc.localize(original_date).astimezone(user_tz)
        # print('converted date: ' + converted_date)

    def test_cron_function(self):
        print('successfully run cron function')