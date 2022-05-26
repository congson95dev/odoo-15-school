from odoo import api, fields, models
from ast import literal_eval

class SchoolSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    school_student_enable_configuration = fields.Boolean(string="Enable Configuration")
    school_student_default_age = fields.Char(string='Age')
    product_default = fields.Many2one('product.product', string='Default Product')
    # many2many will give you multiselect options, when many2one only give you select option
    # to use many2many, we can declare the middle table to connect 2 tables together.
    # in this example, i create a new table named 'config_product_rel'
    # with 2 column connect 2 table that is 'id' for the 'ir_config_parameter' table (current table)
    # and 'product_id' for 'product_product' table
    product_default_many2many = fields.Many2many('product.product', 'config_product_rel', 'id', 'product_id',
                  'Default Product Many2many')

    @api.model
    def get_values(self):
        res = super(SchoolSettings, self).get_values()
        res['school_student_enable_configuration'] = self.env['ir.config_parameter'].sudo().get_param('school.school_student_enable_configuration')
        res['school_student_default_age'] = self.env['ir.config_parameter'].sudo().get_param('school.school_student_default_age')
        res['product_default'] = int(self.env['ir.config_parameter'].sudo().get_param('school.product_default'))

        # set values for many2many field
        if self.env['ir.config_parameter'].sudo().get_param('school.product_default_many2many'):
            product_default_many2many = self.env['ir.config_parameter'].sudo().get_param('school.product_default_many2many')
            res['product_default_many2many'] = [(6, 0, literal_eval(product_default_many2many))]

        return res


    def set_values(self):
        super(SchoolSettings, self).set_values()
        self.env['ir.config_parameter'].set_param('school.school_student_enable_configuration', self.school_student_enable_configuration)
        self.env['ir.config_parameter'].set_param('school.school_student_default_age', self.school_student_default_age)
        # get value for many2one field
        self.env['ir.config_parameter'].set_param('school.product_default', self.product_default.id)
        # get values for many2many field
        self.env['ir.config_parameter'].set_param('school.product_default_many2many', self.product_default_many2many.ids)