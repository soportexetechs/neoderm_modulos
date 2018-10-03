# -*- encoding: UTF-8 -*-
##############################################################################
#
#    Odoo, Open Source Management Solution
#    Copyright (C) 2015-Today Laxicon Solution.
#    (<http://laxicon.in>)
#
#    This program is free software: you can redistribute it and/or modify
#    it under the terms of the GNU General Public License as published by
#    the Free Software Foundation, either version 3 of the License, or
#    (at your option) any later version.
#
#    This program is distributed in the hope that it will be useful,
#    but WITHOUT ANY WARRANTY; without even the implied warranty of
#    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#    GNU General Public License for more details.
#
#    You should have received a copy of the GNU General Public License
#    along with this program.  If not, see <http://www.gnu.org/licenses/>
#
##############################################################################
from odoo import api, models, fields
from datetime import datetime


class sb_patient_recipes(models.Model):
    _name = "sb.patient_recipes"
    _rec_name = "patient"

    recipe_date = fields.Datetime(default=(datetime.today().date()), readonly=True, string='Recipe Date')
    patient = fields.Many2one('res.partner', string='Patient', domain=[('customer', '=', True)], required=True)
    email = fields.Char(string='Email')
    diagnosis = fields.Many2one('sb.common_diagnostics', string='Diagnosis')
    doctor = fields.Many2one('res.partner', string='Doctor', domain=[('supplier', '=', True)])
    # medications_for_recipes = fields.Many2many('sb.medications_for_recipes', 'patient_recipes_medications_for_recipes_rel', 'medications_for_recipes_id', 'patient_recipes_id')
    medication_ids = fields.One2many('sb.medications_for_recipes', 'receipt_id', string="Medications")

    @api.onchange('patient', 'email')
    def patient_onchange(self):
        self.email = self.patient.email_id
        self.doctor = self.patient.family_dr_id or False
        # if self.email and not self.patient.email_id:
        #     self.patient.write({'email_id': self.email})


#   @api.onchange('email','patient')
#   def patient_email(self):
#       if self.patient and  self.email:
#           self.patient.write({'email_id':self.email, 'email':self.email})

    @api.model
    def create(self, vals):
        x = super(sb_patient_recipes, self).create(vals)
        template = self.env['mail.template'].search([('name', '=', 'Patient Receipt E-mail Template')], limit=1)
        if template:
            mail_send = template.send_mail(x.id)
            print (mail_send)
        if self.patient and self.email:
            self.patient.write({'email_id': self.email, 'email': self.email})
        return x

#   @api.model
    def write(self, vals):
        x = super(sb_patient_recipes, self).write(vals)
#       template = self.env['mail.template'].search([('name','=','Patient Receipt E-mail Template')],limit=1)
#       if template:
#               mail_send = template.send_mail(x.id)
        if self.patient and self.email:
            self.patient.write({'email_id': self.email, 'email': self.email})
        return x
