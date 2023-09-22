from odoo import models, fields, api


class HmsPatientStateLog(models.Model):
    _name = "hms.patients.state.log"
    _rec_name = "patient_id"

    patient_id = fields.Many2one('hms.patients')
    description = fields.Char()
    created_by = fields.Char()
    Date = fields.Date()

