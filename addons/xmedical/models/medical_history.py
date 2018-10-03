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


class sb_medical_history(models.Model):
    _name = "sb.medical_history"
    _rec_name = 'patient'

    todays_date = fields.Date(default=datetime.today(), string="Today's Date")
    patient = fields.Many2one('res.partner', string='Patient', required=True, domain=[('customer', '=', True), ('partner_type', '=', 'patient')])
    first_name = fields.Char(string='First Name')
    second_name = fields.Char(string='Second Name')
    surname = fields.Char(string='Surname')
    second_surname = fields.Char(string='Second Surname')
    phone = fields.Char(string='Phone')
    secondary_phone = fields.Char(string='Secondary Phone')
    email = fields.Char(string='Email')
    birth_date = fields.Date(string='BirthDate')
    referred_by = fields.Char(string='Referred By')
    photography = fields.Binary(string='Photography')
    reason_1st_consultation = fields.Char(string='Reason 1st Consultation')
    do_you_have_allergies_to_any_medication_or_food = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Do you have allergies to any medication or food?')
    allergies = fields.Text(string='Allergies')
    have_you_injected_local_anesthesia = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Have you injected local anesthesia?')
    did_you_have_any_adverse_reaction_to_anesthesia = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Did you have any adverse reaction to anesthesia?')
    do_you_currently_take_any_medication = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Do you currently take any medication?')
    pregnancy = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Is pregnancy?')

    medicines = fields.Text(string='Medicines')
    high_pressure = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='High pressure')
    heart_attacks = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Heart attacks')
    bad_coagulation = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Bad coagulation')
    chest_pain = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Chest pain')
    tachycardia = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Tachycardia')
    pacemaker = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Pacemaker')
    smoke = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Smoke')
    bebe = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Bebe')
    drugs = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Drugs')
    specify = fields.Text(string='Specify')
    do_you_have_medical_insurance = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Do you have medical insurance?')
    insurance_name = fields.Many2one('res.partner', string='Insurance Carrier')
    certificate = fields.Char(string='Certificate')
    policy = fields.Char(string='Policy')
    bronchitis = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Bronchitis')
    asthma = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Asthma')
    emphysema = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Emphysema')
    difficulty_breathing = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Difficulty breathing')
    diabetes = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Diabetes')
    kidneys = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Kidneys')
    seizures_epilepsy = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Seizures, Epilepsy')
    urinary_infections = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Urinary infections')
    cancer = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Cancer')
    thyroid = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Thyroid')
    arthritis = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Arthritis')
    fainting = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Fainting')
    hepatitis = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Hepatitis')
    some_other_condition = fields.Text(string='Some Other Condition')
    skin_cancer = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Skin cancer')
    familiar_with_skin_cancer = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Familiar with skin cancer')
    relationship = fields.Char(string='Relationship')
    bleed_easily = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Bleed easily')
    specific_disease = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Specific disease')
    which = fields.Char(string='Which')
    keloid_healing = fields.Selection([('yes', 'Yes'), ('no', 'No')], string='Keloid healing')
    operations = fields.Text(string='Operations')

    # @api.onchange('patient')
    # def change_history_status1(self):
    #     print ("patient11111", self.patient)
    #     if self.patient:
    #         self.patient.state_medical_history = 'completed'

    @api.onchange('email', 'patient')
    def email_onchange(self):
        if self.email and self.patient.email_id != self.email:
            p = self.env['res.partner'].search([('id', '=', self.patient.id)], limit=1)
            p.write({'email_id': self.email})

    @api.onchange('phone', 'patient')
    def phone_onchange(self):
        if self.phone and self.patient.phone_no != self.phone:
            p = self.env['res.partner'].search([('id', '=', self.patient.id)], limit=1)
            p.write({'phone_no': self.phone})

    @api.onchange('first_name', 'patient')
    def first_name_onchange(self):

        if self.first_name and self.patient.first_name != self.first_name:
            p = self.env['res.partner'].search([('id', '=', self.patient.id)], limit=1)
            p.write({'first_name': str(self.first_name).title()})

    @api.onchange('second_name', 'patient')
    def second_name_onchange(self):
        if self.second_name and self.patient.second_name != self.second_name:
            p = self.env['res.partner'].search([('id', '=', self.patient.id)], limit=1)
            p.write({'second_name': str(self.second_name).title()})

    @api.onchange('surname', 'patient')
    def surname_onchange(self):
        if self.surname and self.patient.surname != self.surname:
            p = self.env['res.partner'].search([('id', '=', self.patient.id)], limit=1)
            p.write({'surname': str(self.surname).title()})

    @api.onchange('second_surname', 'patient')
    def second_surname_onchange(self):
        if self.second_surname and self.patient.second_surname != self.second_surname:
            p = self.env['res.partner'].search([('id', '=', self.patient.id)], limit=1)
            p.write({'second_surname': str(self.second_surname).title()})

    @api.onchange('patient')
    def patient_onchange(self):
        self.first_name = self.patient.first_name
        self.second_name = self.patient.second_name
        self.surname = self.patient.surname
        self.second_surname = self.patient.second_surname
        self.phone = self.patient.phone_no
        self.secondary_phone = self.patient.secondary_phone
        self.email = self.patient.email_id
        self.birth_date = self.patient.birth_date
        self.referred_by = self.patient.referred_by
        self.insurance_name = self.patient.insurance_carrier.id if self.patient.insurance_carrier else False

    @api.model
    def create(self, vals):
        res = super(sb_medical_history, self).create(vals)
        if res.patient:
            if self.phone:
                res.patient.phone = self.phone

            if self.secondary_phone:
                res.patient.secondary_phone = self.secondary_phone

            if self.email:
                res.patient.email_id = self.email
            res.patient.state_medical_history = 'completed'

        return res

    def write(self, vals):
        data = {}
        if vals.get('phone', False):
            data['phone'] = vals['phone']

        if vals.get('secondary_phone', False):
            data['secondary_phone'] = vals['secondary_phone']

        if vals.get('email', False):
            data['email_id'] = vals['email']
        if vals.get('patient', False):
            data['state_medical_history'] = 'completed'

        x = super(sb_medical_history, self).write(vals)
        self.patient.write(data)

        return x
