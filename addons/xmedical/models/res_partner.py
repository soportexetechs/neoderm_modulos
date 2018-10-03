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

from odoo import api, fields, models
from datetime import datetime
from ast import literal_eval


class ResPartner(models.Model):
    _inherit = "res.partner"
    _rec_name = "sb_name"

    @api.multi
    def compute_medical_history(self, *args):
        _h = self.env['sb.medical_history']
        for r in self:
            ids = _h.search([('patient', '=', r.id)]).ids
            if ids:
                r.no_of_medical_history = len(ids)

    @api.multi
    def compute_appointments(self, *args):
        _h = self.env['sb.appointment_calender']
        for r in self:
            ids = _h.search([('patient_id', '=', r.id)]).ids
            if ids:
                r.no_of_appointments = len(ids)

    @api.multi
    def compute_diagnostics(self, *args):
        _h = self.env['sb.patient_diagnostics']
        for r in self:
            ids = _h.search([('patient', '=', r.id)]).ids
            if ids:
                r.no_of_diagnostics = len(ids)

    @api.multi
    def compute_recipes(self, *args):
        _h = self.env['sb.patient_recipes']
        for r in self:
            ids = _h.search([('patient', '=', r.id)]).ids
            if ids:
                r.no_of_recipes = len(ids)

    @api.multi
    def total_name(self, *args):
        for x in self:
            if x.partner_type == 'patient':
                x.sb_name = str("%s %s %s %s " % (x.first_name or '', x.second_name or '', x.surname or '', x.second_surname or '')).title()
                x.name = x.sb_name

    @api.multi
    def age_calculate(self):
        for x in self:
            if x.birth_date:
                a = datetime.strptime(x.birth_date, "%Y-%m-%d")
                val = (datetime.now() - a).days / 365

                if (val <= 0):
                    x.age = 0.0
                else:
                    x.age = val

    # @api.multi
    # def compute_update_state(self):
    #     _h = self.env['sb.medical_history']
    #     for x in self:
    #         x.state_medical_history = 'completed' if _h.search([('patient', '=', x.id)]).ids else 'pending'

    sb_name = fields.Char(string='Name', required=False, readonly=False, compute="total_name")
    first_name = fields.Char(string='First Name')
    second_name = fields.Char(string='Second Name')
    surname = fields.Char(string='Surname')
    second_surname = fields.Char(string='Second Surname')
    phone_no = fields.Char(string='Phone')
    secondary_phone = fields.Char(string='Secondary Phone')
    email_id = fields.Char(string='Email')
    birth_date = fields.Date(string='BirthDate')
    age = fields.Integer(readonly=True, string='Age', compute="age_calculate")
    no_current_file = fields.Integer(string='No. Current File')
    referred_by = fields.Char(string='Referred By')
    name_to_invoice = fields.Char(string='Name To Invoice')
    nit = fields.Char(string='NIT')
    billing_address = fields.Text(string='Billing Address')
    insurance_carrier = fields.Many2one('res.partner', string='Insurance Carrier')
    certificate = fields.Char(string='Certificate')
    policy = fields.Char(string='Policy')
    doctor_speciality = fields.Char(string='Speciality Fields')
    state_medical_history = fields.Selection([('pending', 'Pending'), ('completed', 'Completed')], default='pending', string='State Medical History')
    partner_type = fields.Selection([('insura', 'Insurance'), ('doctor', 'Doctor'), ('patient', 'Patient')], string='Partner Type')
    no_of_medical_history = fields.Integer(default=0, compute='compute_medical_history')
    no_of_appointments = fields.Integer(default=0, compute='compute_appointments')
    no_of_diagnostics = fields.Integer(default=0, compute='compute_diagnostics')
    no_of_recipes = fields.Integer(default=0, compute='compute_recipes')
    family_dr_id = fields.Many2one('res.partner', string="Family Doctor")

    @api.onchange('first_name', 'second_name', 'surname', 'second_surname', 'name', 'name_to_invoice')
    def onchange_name_base_id(self):
        if self.first_name:
            self.first_name = str(self.first_name).title()
        if self.second_name:
            self.second_name = str(self.second_name).title()
        if self.surname:
            self.surname = str(self.surname).title()
        if self.second_surname:
            self.second_surname = str(self.second_surname).title()
        if self.name_to_invoice:
            self.name_to_invoice = str(self.name_to_invoice).title()
        if self.partner_type == 'patient':
            self.name = str("%s %s %s %s" % (self.first_name or '',
                                             self.second_name or '',
                                             self.surname or '',
                                             self.second_surname or '')).title() if self.partner_type == 'patient' else self.name

    # @api.onchange('birth_date','age')
    # def onchange_getage_id(self):
    #   if self.birth_date:
    #       a = datetime.strptime(self.birth_date, "%Y-%m-%d")
    #       self.age = (datetime.now() - a).days / 365

#   @api.model
#   def create(self, vals):
#       x = super(res_partner, self).create(vals)
#       if x.first_name or x.surname:
#           x.name = "%s %s %s %s "%(x.first_name or '', x.second_name or '', x.surname or '', x.second_surname or '')
#       return x

#   @api.model
    def write(self, vals):
        if self.partner_type == 'patient':
            vals['name'] = "%s %s %s %s " % (vals.get('first_name', self.first_name or ''),
                                             vals.get('second_name', self.second_name or ''),
                                             vals.get('surname', self.surname or ''),
                                             vals.get('second_surname', self.second_surname or ''))
        x = super(ResPartner, self).write(vals)
        return x

    @api.multi
    def action_view_medical_history(self):
        medical_ids = self.env['sb.medical_history'].search([('patient', '=', self.id)]).ids
        self.ensure_one()
        result = self.env.ref('xmedical.sb_medical_history_action').read()[0]
        result['domain'] = literal_eval(result['domain'])
        result['domain'].append(('id', 'in', medical_ids))
        return result

    @api.multi
    def action_view_patient_diagnoses(self):
        diagnoses_ids = self.env['sb.patient_diagnostics'].search([('patient', '=', self.id)]).ids
        self.ensure_one()
        result = self.env.ref('xmedical.sb_patient_diagnostics_action').read()[0]
        result['domain'] = literal_eval(result['domain'])
        result['domain'].append(('id', 'in', diagnoses_ids))
        return result

    @api.multi
    def action_view_patient_appoinment(self):
        diagnoses_ids = self.env['sb.appointment_calender'].search([('patient', '=', self.id)]).ids
        self.ensure_one()
        result = self.env.ref('xmedical.sb_appointment_calender_action').read()[0]
        result['domain'] = literal_eval(result['domain'])
        result['domain'].append(('id', 'in', diagnoses_ids))
        return result

    @api.multi
    def action_view_patient_recipes(self):
        recipes_ids = self.env['sb.patient_recipes'].search([('patient', '=', self.id)]).ids
        self.ensure_one()
        result = self.env.ref('xmedical.sb_patient_recipes_action').read()[0]
        result['domain'] = literal_eval(result['domain'])
        result['domain'].append(('id', 'in', recipes_ids))
        return result
