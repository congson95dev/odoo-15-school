from odoo import api, models, fields, _
from odoo.exceptions import ValidationError

class Calendar(models.Model):
    _name = "school.calendar"
    _description = "Calendar"

    # when you inherit other modules, you must add it in depends in __manifest__.py
    _inherit = ['mail.thread', 'mail.activity.mixin']

    # _rec_name is use for defind default "name" if the model don't have "name" field.
    # if we don't add this _rec_name, the default name display will be _name,id, Ex: school.calendar,1
    _rec_name="sequence"
    _order = "sequence desc"

    # override default value of field
    # this function MUST added before we define the field
    @api.model
    def default_get(self, fields):
        res = super(Calendar, self).default_get(fields)
        # set default value for field description
        res['description'] = 'Test Description'
        return res

    sequence = fields.Char(string='Sequence', required=True, copy=False, readonly=True, index=True, default=lambda self: _('New'), tracking=True)
    # ondelete have 2 method:
    # ondelete="restrict" will prevent you from delete student if that student is currently connecting to some calendars
    # ondelete="cascade" will delete calendars which connected with the deleted student
    student_id = fields.Many2one('school.students', string='Student', required=True, tracking=True, ondelete="cascade")
    teacher_id = fields.Many2one('school.teachers', string='Teachers', required=True, tracking=True)
    student_age = fields.Integer(string='Age', related='student_id.student_age', tracking=True)
    student_gender = fields.Selection([('m', 'Male'), ('f', 'Female'), ('o', 'Other')], string='Gender', tracking=True)
    date = fields.Datetime(string='Date', tracking=True)
    state = fields.Selection([
        ('draft', 'Draft'),
        ('confirm', 'Confirm'),
        ('done', 'Done'),
        ('cancel', 'Cancel')
    ], string='Status', default='draft', tracking=True)
    product_id = fields.Many2one('product.template', string='Product', tracking=True)
    # - one2many field will show a field that we can add multiple value
    # - syntax was somename_ids, there's always have _ids at the end
    # - when we create a one2many field, we also need to create a many2one field in another model and connect it to eachother
    calendar_jobs_ids = fields.One2many('calendar.jobs', 'calendar_id', string="Jobs")
    school_products_ids = fields.One2many('school.products', 'calendar_id', string="Products")
    description = fields.Html(string="Description")
    hide_priority_column = fields.Boolean(string="Hide Priority Column In Page 1")
    color_picker = fields.Integer(string="Color Picker")
    color = fields.Integer(string="Color")
    # text field is bigger than normal char field
    text_field = fields.Text(string="Text Field")

    # override function create
    @api.model
    def create(self, vals):
        # show sequence
        if vals.get('sequence', _('New')) == _('New'):
            # the name inside next_by_code is get by file data/sequence.xml
            vals['sequence'] = self.env['ir.sequence'].next_by_code('school.calendar') or _('New')

        res = super(Calendar, self).create(vals)
        return res

    def unlink(self):
        # ignore if it's in done state
        if (self.state == 'done'):
            # to use this ValidationError, you have to import it first
            raise ValidationError(_('You cannot delete this record because its in Done state.'))
        return super(Calendar, self).unlink()

    @api.onchange('student_id')
    def onchange_student_id(self):
        # change student_gender when choose student
        # we could use "related" in view file instead, but in this course, i just wanna do it with onchange api
        # note: when you use this way to change value of a field, and that field is readonly="1", you must add force_save to that field
        if self.student_id:
            if self.student_id.student_gender:
                self.student_gender = self.student_id.student_gender
        else:
            self.student_gender = ''

    @api.onchange('product_id')
    def onchange_product_id(self):
        # change one2many field based many2one field change
        # change school_products_ids when choose product_id
        for rec in self:
            # [(5, 0, 0)] is to remove all existing record and only save the new record only
            lines = [(5, 0, 0)]
            vals = {
                'name' : rec.product_id.name,
                'qty': 1
            }
            line = (0, 0, vals)
            lines.append(line)
            rec.school_products_ids = lines

    def action_draft(self):
        for rec in self:
            if rec.state == 'cancel':
                rec.state = 'draft'

    def action_confirm(self):
        self.state = 'confirm'
        # show rainbow_man effect after set status to "confirm"
        return {
            'effect': {
                'fadeout': 'slow',
                'message': 'Set to confirm successfully',
                'type': 'rainbow_man',
            }
        }

    def action_done(self):
        self.state = 'done'

    def action_cancel(self):
        for rec in self:
            if rec.state in ('draft','confirm','done'):
                self.state = 'cancel'

    # count calendar jobs by calendar id
    def count_jobs(self):
        return self.env['calendar.jobs'].search_count([('calendar_id','=',self.id)])

    def send_calendar_info_email(self):
        # get email template id by record id in data/mail_template_data.xml
        template_id = self.env.ref('school.email_template_calendar_info').id
        # send email by function send_mail
        self.env['mail.template'].browse(template_id).send_mail(self.id, force_send=True)

    def clear_all_jobs(self):
        for record in self:
            record.calendar_jobs_ids = [(5,0,0)]

# this class is created for serve one2many field "calendar_jobs_ids" in model above
class CalendarJobs(models.Model):
    _name = "calendar.jobs"
    _description = "Calendar Jobs"

    # sequence is created so we can use it for widget="handle" in tree view
    sequence = fields.Char(string='Sequence')
    name = fields.Char(string='Name', required=True)
    priority = fields.Char(string='Priority')
    # this field is created for connect to one2many field "calendar_jobs_ids" in model above
    # hide this field in form and tree view if you don't wanna see it
    calendar_id = fields.Many2one('school.calendar', string='Calendar Id')

# this class is created for serve one2many field "school_products" in model above
class SchoolProducts(models.Model):
    _name = "school.products"
    _description = "School Products"

    # sequence is created so we can use it for widget="handle" in tree view
    sequence = fields.Char(string='Sequence')
    name = fields.Char(string='Name')
    qty = fields.Char(string='Qty')
    # this field is created for connect to one2many field "school_products_ids" in model above
    # hide this field in form and tree view if you don't wanna see it
    calendar_id = fields.Many2one('school.calendar', string='Calendar Id')
