from odoo import api, models, fields, _
from odoo.exceptions import ValidationError

class Teachers(models.Model):
    _name = "school.teachers"
    _description = "Teachers"

    # when you inherit other modules, you must add it in depends in __manifest__.py
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # tracking=True is track whenever you change the data of record
    # it will make a note that show what has been changed in chatbox in bottom of the edit form view
    # but you will need to make a chatbox so this tracking note can be show

    # copy = False is to ignore from copy() function
    # when you add this copy = False, the attribute won't be copy when you click dupplicate

    # this field is for sequence id
    sequence = fields.Char(string='Sequence', required=True, copy=False, readonly=True,
                       states={'draft': [('readonly', False)]}, index=True, default=lambda self: _('New'), tracking=True)
    teacher_id = fields.Many2one('res.users', string='Teachers', required=True, tracking=True)
    name = fields.Char(string='Name', related='teacher_id.name', tracking=True)
    photo = fields.Binary(string='Photo', related='teacher_id.image_1920', tracking=True)
    teacher_age = fields.Integer(string='Age', tracking=True, copy=False)
    teacher_dob = fields.Date(string="Date of Birth", related='teacher_id.birthday', tracking=True)
    teacher_gender = fields.Selection([('male', 'Male'), ('female', 'Female'), ('other', 'Other')], string='Gender', related='teacher_id.gender', tracking=True, store=True)
    teacher_blood_group = fields.Selection(
        [('A+', 'A+ve'), ('B+', 'B+ve'), ('O+', 'O+ve'), ('AB+', 'AB+ve'),
         ('A-', 'A-ve'), ('B-', 'B-ve'), ('O-', 'O-ve'), ('AB-', 'AB-ve')],
        string='Blood Group', tracking=True)
    teacher_calendar_count = fields.Integer(string="Calendar Count", compute="_compute_teacher_calendar_count", tracking=True)
    nationality = fields.Many2one('res.country', string='Nationality', related='teacher_id.private_country_id', tracking=True)
    calendar_ids = fields.One2many('school.calendar', 'teacher_id', string="Calendars")
    # show archive / unarchive in list
    active = fields.Boolean(string="Active", default=True)
    teacher_calendar_many2many = fields.Many2many('school.calendar', string='Teacher Calendar Many2many')

    # compute function
    def _compute_teacher_calendar_count(self):
        # count teacher_calendar_count
        for record in self:
            teacher_calendar_count = self.env['school.calendar'].search_count([('teacher_id','=',record.id)])
            record.teacher_calendar_count = teacher_calendar_count

    # override function create
    @api.model
    def create(self, vals):
        # show sequence
        if vals.get('sequence', _('New')) == _('New'):
            # the name inside next_by_code is get by file data/sequence.xml
            vals['sequence'] = self.env['ir.sequence'].next_by_code('school.teachers') or _('New')

        res = super(Teachers, self).create(vals)
        return res

    # override function copy
    def copy(self, default=None):
        self.ensure_one()
        default = dict(default or {})
        if 'name' not in default:
            # add (copy) after name
            default['name'] = _("%s (copy)") % (self.name)
        return super(Teachers, self).copy(default=default)

    # override function name_get
    # this function work when we click on dropdown which listed the records of this model
    # Ex: create new calendar -> click on teachers dropdown
    def name_get(self):
        result = []
        for record in self:
            # add sequence before name
            # Ex: [S00001] teacher 1
            name = '[' + record.sequence + '] ' + record.name
            result.append((record.id, name))
        return result

    # issue when use constrains to many2one field that it trigger on every action in the page
    # @api.constrains('teacher_id')
    # def check_teacher_id(self):
    #     # check if name exists in db, then throw error
    #     for record in self:
    #         # we need the ('id','!=',record.id) because we need to remove current record from the constrain
    #         # or else, it will always found the record
    #         # this only happen in contrains
    #         teacher = self.env['school.teachers'].search([('teacher_id','=',record.teacher_id.id),('id','!=',record.id)])
    #         if (teacher):
    #             raise ValidationError(_('Teachers %s is already registered', self.name))

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
            'domain': [('teacher_id', '=', self.id)],
            # this will pass default teacher_id to the form view when you click "Create" button after go to list view by Smart Button
            # so when you click "Create" button, the form will auto filled all the teacher data for you
            # syntax: default_{some_field}
            'context': {'default_teacher_id': self.id},
        }