from odoo import api, fields, models
from ast import literal_eval

class SchoolSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    school_student_enable_configuration = fields.Boolean(string="Enable Configuration")
    school_student_default_age = fields.Char(string='Age')
    # Trying to make Many2many field in settings, but doesn't work
    # Link and issue: https://www.youtube.com/watch?v=-n7Ttx1Czdw&list=PLqRRLx0cl0hoJhjFWkFYowveq2Zn55dhM&index=96
    # product_default = fields.Many2many('product.product', string='Default Product')

    @api.model
    def get_values(self):
        res = super(SchoolSettings, self).get_values()
        res['school_student_enable_configuration'] = self.env['ir.config_parameter'].sudo().get_param('school.school_student_enable_configuration')
        res['school_student_default_age'] = self.env['ir.config_parameter'].sudo().get_param('school.school_student_default_age')

        # Trying to make Many2many field in settings, but doesn't work
        # Link and issue: https://www.youtube.com/watch?v=-n7Ttx1Czdw&list=PLqRRLx0cl0hoJhjFWkFYowveq2Zn55dhM&index=96
        # if self.env['ir.config_parameter'].sudo().get_param('school.school_default_teacher'):
        #     product_default = self.env['ir.config_parameter'].sudo().get_param('school.product_default')
        #     res.update(
        #         product_default=[(6, 0, literal_eval(product_default))]
        #     )

        return res


    def set_values(self):
        super(SchoolSettings, self).set_values()
        self.env['ir.config_parameter'].set_param('school.school_student_enable_configuration', self.school_student_enable_configuration)
        self.env['ir.config_parameter'].set_param('school.school_student_default_age', self.school_student_default_age)
        # Trying to make Many2many field in settings, but doesn't work
        # Link and issue: https://www.youtube.com/watch?v=-n7Ttx1Czdw&list=PLqRRLx0cl0hoJhjFWkFYowveq2Zn55dhM&index=96
        # self.env['ir.config_parameter'].set_param('school.product_default', self.product_default.ids)