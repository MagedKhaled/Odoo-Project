from odoo import models,fields

class Hmsdepartment(models.Model):
    _name = 'hms.departments'
    name = fields.Char()
    capacity = fields.Integer()
    is_opened = fields.Boolean()
    # patient_ids = fields.One2many(comodel_name='hms.patients',inverse_name='department_id')