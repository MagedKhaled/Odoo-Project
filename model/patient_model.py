from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime
import re
class HmsPatient(models.Model):
    _name = "hms.patients"
    _rec_name = "first_name"

    first_name = fields.Char()
    last_name = fields.Char()
    birth_date = fields.Date()
    history = fields.Html()
    cr_ratio = fields.Float()
    blood_type = fields.Selection([('A','A'),('B','B'),('AB','AB'),('O','O')])
    PCR = fields.Boolean()
    image = fields.Image()
    address = fields.Char()
    age = fields.Integer(compute='age_auto_detect')
    department_id = fields.Many2one(comodel_name='hms.departments')
    doctor_id = fields.Many2many(comodel_name='hms.doctors')
    department_capacity = fields.Integer(related="department_id.capacity")

    state = fields.Selection([('Undetermined','Undetermined'),('Good','Good'),('Fair','Fair'),('Serious','Serious')])
    state_log = fields.One2many('hms.patients.state.log','patient_id')

    email = fields.Char(unique=True)

    @api.onchange('age')
    def set_PCR(self):
        if (self.age < 30) and not (self.age == 0):
            self.PCR = True
            return {
                
                'warning':{
                    
                    'title': ('PCR is checked'),
                    'message': 'You age is less than 30'

                }
            }
        else:
            self.PCR = False
        


    @api.onchange('state')
    def create_state_log(self):
        for rec in self:
            vals = {
                'description':'state changed to %s'%(rec.state),
                'patient_id': rec.id 
            }
            rec.env['hms.patients.state.log'].create(vals)




    @api.onchange('email')
    def email_validation(self):
        if self.email:
            match = re.match("^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$",self.email)
            if not match:
                raise ValidationError('The Email is invalide!')



    @api.depends("birth_date")
    def age_auto_detect(self):
        for record in self:
            if record.birth_date:
                birth_date = record.birth_date.strftime('%Y-%m-%d')
                birth_date = datetime.strptime(birth_date, '%Y-%m-%d').date()
                today = datetime.today().date()
                record.age = today.year - birth_date.year
                 
            else:
                record.age = 0  

        

    