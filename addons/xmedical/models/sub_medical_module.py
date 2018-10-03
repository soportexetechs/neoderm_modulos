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

from odoo import fields, models
from datetime import datetime


class sb_patient_diagnostics(models.Model):
    _name = "sb.patient_diagnostics"
    _inherit = ['mail.thread']
    _rec_name = "diagnostics_date"

    diagnostics_date = fields.Date(default=datetime.today(), readonly=True, string='Diagnostics Date')
    patient = fields.Many2one('res.partner', string='Patient', domain=[('customer', '=', True)], required=True)
    diagnosis = fields.Many2one('sb.common_diagnostics', string='Diagnosis')
    doctor = fields.Many2one('res.partner', string='Doctor', domain=[('supplier', '=', True)])
    reference_image = fields.Binary(string='Reference Image')
    observations = fields.Text(string='Observations')


#   @api.model
#   def create(self, vals):
#       x = super(sb_patient_diagnostics, self).create(vals)
#       template = self.env['mail.template'].search([('name','=','Patient Diagnostics E-mail Template')],limit=1)
#       if template:
#               mail_send = template.send_mail(x.id)
#       return x


class sb_insurance_companies_list(models.Model):
    _name = "sb.insurance_companies_list"

    name = fields.Char(string="Insurance Compnay")


class sb_appointment_types(models.Model):
    _name = "sb.appointment_types"

    name = fields.Char(string="Name")


class sb_common_diagnostics(models.Model):
    _name = "sb.common_diagnostics"
    _rec_name = 'diagnosis'

    diagnosis = fields.Char(string="Diagnosis")


class sb_sales_channel(models.Model):
    _name = "sb.sales_channel"

    name = fields.Char(string="Name")


class sb_medications_for_recipes(models.Model):
    _name = "sb.medications_for_recipes"

    medicine = fields.Many2one('sb.medicines', string='Medicine', required=True)
    quantity = fields.Float(string='Quantity', default=1.0, required=True)
    indications = fields.Char(string='Indications', required=True)
    presentation = fields.Char(string='Presentation')
    concentration = fields.Char(string='Concentration')
    receipt_id = fields.Many2one('sb.patient_recipes', 'concentration')

#   @api.onchange('medicine','indications', 'presentation', 'email')
#   def on_change_medicine(self):
#       self.indications = self.medicine.indications
#       self.presentation = self.medicine.presentation
#       self.concentration = self.medicine.concentration


class sb_medicines(models.Model):
    _name = "sb.medicines"

    name = fields.Char(string="Medicine", required=True)
    indications = fields.Char(string='Indications', required=True)
    presentation = fields.Char(string='Presentation')
    concentration = fields.Char(string='Concentration')
