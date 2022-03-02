from odoo import api, fields, models

class SchoolSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    school_student_enable_configuration = fields.Boolean(string="Enable Configuration")
    school_student_default_age = fields.Char(string='Age')

    @api.model
    def get_values(self):
        res = super(SchoolSettings, self).get_values()
        res['school_student_enable_configuration'] = self.env['ir.config_parameter'].sudo().get_param('school.school_student_enable_configuration')
        res['school_student_default_age'] = self.env['ir.config_parameter'].sudo().get_param('school.school_student_default_age')

        return res


    def set_values(self):
        super(SchoolSettings, self).set_values()
        self.env['ir.config_parameter'].set_param('school.school_student_enable_configuration', self.school_student_enable_configuration)
        self.env['ir.config_parameter'].set_param('school.school_student_default_age', self.school_student_default_age)