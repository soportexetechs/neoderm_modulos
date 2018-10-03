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

from odoo import api, fields, models, _
from datetime import datetime
import pytz
from openerp.exceptions import UserError
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT, DEFAULT_SERVER_DATE_FORMAT

TIME_SLOT = []


class sb_appointment_calender(models.Model):
    _name = "sb.appointment_calender"
    _inherit = ['mail.thread']

    @api.depends('start_date', 'start_time', 'end_time')
    def get_appoinment_date_time(self):
        for rec in self:
            if rec.start_time and rec.start_date:
                final_date = rec.start_date + " " + rec.start_time.start_time
                end_time = rec.start_date + " " + rec.start_time.end_time
                if self.end_time:
                    end_time = self.start_date + " " + self.end_time.start_time
            # self.appointment_date = datetime.strptime(final_date, DEFAULT_SERVER_DATETIME_FORMAT)
            # self.appointment_duration = datetime.strptime(end_time, DEFAULT_SERVER_DATETIME_FORMAT)
                rec.appointment_date = final_date
                rec.appointment_duration = end_time

    name = fields.Char('Appointment Summery...', required=True)
    phone = fields.Char('Phone')
    email = fields.Char('Email')
    patient_id = fields.Many2one('res.partner', string='Patient', domain=[('customer', '=', True)], required=True)
    dr_id = fields.Many2one('res.partner', string='Doctor', domain=[('supplier', '=', True)], required=True)
    insurance_note = fields.Many2one('res.partner', string='Insurance Carrier')
    appointment_type_id = fields.Many2one('sb.appointment_types', string="Appointment Type", required=True)
    start_date = fields.Date(string="Appointment Date")
    start_time = fields.Many2one('time.slot.line', string="From Time")
    end_time = fields.Many2one('time.slot.line', string=" To Time")
    # appointment_all_day = fields.Boolean('All Day')
    state = fields.Selection([('draft', 'Draft'), ('scheduled', 'Scheduled'), ('confirmed', 'Confirmed'), ('in_waiting_room', 'In Waiting Room'), ('with_doctor', 'With Doctor'), ('finished', 'Finished')], default="draft", required=True)
    color = fields.Integer('Color Index', compute="change_colore_on_kanban")
    appointment_date = fields.Datetime(string="Start Time", readonly=True, compute='get_appoinment_date_time')
    appointment_duration = fields.Datetime(string="End Time", compute='get_appoinment_date_time')

    @api.multi
    @api.onchange('start_date', 'dr_id')
    def onchange_date(self):
        time_ids = []
        if self.start_date:
            if self.start_date < fields.Date.today():
                raise UserError(_("You can not select privious Date for Appoinmnet"))
        if self.start_date and self.dr_id:
            self.start_time = False
            self.end_time = False
            tz = pytz.timezone(self.env.user.partner_id.tz)
            start_period = pytz.utc.localize(datetime.strptime(self.start_date, DEFAULT_SERVER_DATE_FORMAT)).astimezone(tz)
            day = start_period.weekday()
            slot_id = self.env['time.slot.management'].search([('name', '=', self.dr_id.id)], limit=1)
            time_slot_line_obj = self.env['time.slot.line']
            domain = ""
            if day == 1:
                domain = [('monday_time_slot_id', '=', slot_id.id)]
            elif day == 2:
                domain = [('tuesday_time_slot_id', '=', slot_id.id)]
            elif day == 3:
                domain = [('wednesday_time_slot_id', '=', slot_id.id)]
            elif day == 4:
                domain = [('thursday_time_slot_id', '=', slot_id.id)]
            elif day == 5:
                domain = [('friday_time_slot_id', '=', slot_id.id)]
            elif day == 6:
                domain = [('saturday_time_slot_id', '=', slot_id.id)]
            elif day == 0:
                domain = [('sunday_time_slot_id', '=', slot_id.id)]
            time_ids = time_slot_line_obj.search(domain).ids
        return {'domain': {'start_time': [('id', 'in', time_ids)]}}

    @api.multi
    @api.onchange('start_date', 'dr_id', 'start_time', 'end_time')
    def _onchange_time(self):
        if self.start_time and self.start_date and self.end_time:
            final_date = self.start_date + " " + self.start_time.start_time
            end_time = self.start_date + " " + self.start_time.end_time
            if self.end_time:
                end_time = self.start_date + " " + self.end_time.start_time
            # self.appointment_date = datetime.strptime(final_date, DEFAULT_SERVER_DATETIME_FORMAT)
            # self.appointment_duration = datetime.strptime(end_time, DEFAULT_SERVER_DATETIME_FORMAT)
            self.appointment_date = final_date
            self.appointment_duration = end_time

    @api.multi
    @api.onchange('state')
    def change_colore_on_kanban(self):
        for record in self:
            color = 0
            if record.state == 'draft':
                color = 1
            elif record.state == 'scheduled':
                color = 2
            elif record.state == 'confirmed':
                color = 3
            elif record.state == 'in_waiting_room':
                color = 4
            elif record.state == 'with_doctor':
                color = 5
            elif record.state == 'finished':
                color = 6
            else:
                color = 7
            record.color = color

    @api.onchange('patient_id', 'insurance_note', 'phone', 'email')
    def onchange_patient_id(self):
        self.insurance_note = self.patient_id.insurance_carrier.id if self and self.patient_id and self.patient_id.insurance_carrier else False
        self.email = self.patient_id.email_id
        self.phone = self.patient_id.phone_no
        self.insurance_note = self.patient_id.insurance_carrier.id
        self.dr_id = self.patient_id.family_dr_id or False

    @api.model
    def create(self, vals):
        print ("valse", vals)
        x = super(sb_appointment_calender, self).create(vals)
        template = self.env['mail.template'].search([('name', '=', 'Appointment E-mail Template')], limit=1)
        if template:
            mail_send = template.send_mail(x.id)
            print (mail_send)
        return x

    @api.multi
    def appoinment_scheduled(self):
        self.write({'state': 'scheduled'})

    @api.multi
    def appoinment_confirmed(self):
        self.write({'state': 'confirmed'})

    @api.multi
    def appoinment_in_waiting_room(self):
        self.write({'state': 'in_waiting_room'})

    @api.multi
    def appoinment_with_doctor(self):
        self.write({'state': 'with_doctor'})

    @api.multi
    def appoinment_finished(self):
        self.write({'state': 'finished'})

    # def write(self, vals):
        # from datetime import time
        # get user's timezone
        # tz = pytz.timezone(self.env.user.partner_id.tz)
        # get localized dates
        # if not vals.get('start_date', self.start_date) or not vals.get('end_date', self.end_date):
        # raise UserError(_("For Appointment Booking Start Date and End Date Both Required."))
        # date_from = pytz.utc.localize(datetime.strptime(vals.get('start_date', self.start_date), DEFAULT_SERVER_DATETIME_FORMAT)).astimezone(tz)
        # date_to = pytz.utc.localize(datetime.strptime(vals.get('end_date', self.end_date), DEFAULT_SERVER_DATETIME_FORMAT)).astimezone(tz)
        # start_time = date_from.time()
        # end_time = date_to.time()
        # if start_time < time(7, 00) or start_time > time(19, 00):
        #     raise UserError(_("Appointment Booking Only Valid Within 7AM-7PM A day."))
        # x = super(sb_appointment_calender, self).write(vals)
        # return x

    def sb_appointment_reminder(self):
        tomorrow = datetime.today() + datetime.timedelta(days=1)
        appointments = self.env['sb.appointment_calender'].search(
                [('start_date', '>=', tomorrow.strftime("%Y-%m-%d 00:00:00")), ('start_date', '<=', tomorrow.strftime("%Y-%m-%d 12:59:59"))])
        template = self.env['mail.template'].search([('name', '=', 'Appointment Reminder Template')], limit=1)
        for a in appointments:
            if template:
                mail_send = template.send_mail(a.id)
                print (mail_send)
