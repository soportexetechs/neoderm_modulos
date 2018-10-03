

from odoo import api, models, _, fields
from datetime import datetime, time, timedelta
from openerp.exceptions import UserError
import pytz
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT








class sb_appointment_calender(models.Model):
    _name = "sb.appointment_calender"
    _inherit = ['mail.thread']

    name = fields.Char('Appointment Summery...', required=True)
    phone = fields.Char('Phone')
    email = fields.Char('Email')
    patient_id = fields.Many2one('res.partner', string='Patient', domain=[('customer', '=', True)], required=True)
    insurance_note = fields.Many2one('res.partner', string='Insurance Carrier')
    appointment_type_id = fields.Many2one('sb.appointment_types', string="Appointment Type", required=True)
    start_date = fields.Datetime(string="Start Date")
    end_date = fields.Datetime(string="End Date")
    appointment_duration = fields.Float('Duration')
    appointment_all_day = fields.Boolean('All Day')

    _rec_name = 'name'

    @api.onchange('patient_id', 'insurance_note', 'phone', 'email')
    def onchange_patient_id(self):
        self.insurance_note = self.patient_id.insurance_carrier.id if self and self.patient_id and self.patient_id.insurance_carrier else False
        self.email = self.patient_id.email_id
        self.phone = self.patient_id.phone_no
        self.insurance_note = self.patient_id.insurance_carrier.id

    @api.model
    def create(self, vals):
        x = super(sb_appointment_calender, self).create(vals)
        template = self.env['mail.template'].search([('name', '=', 'Appointment E-mail Template')], limit=1)
        if template:
            mail_send = template.send_mail(x.id)
            print (mail_send)
        return x

    def write(self, vals):
        # from datetime import time
        # get user's timezone
        tz = pytz.timezone(self.env.user.partner_id.tz)
        # get localized dates
        if not vals.get('start_date', self.start_date) or not vals.get('end_date', self.end_date):
            raise UserError(_("For Appointment Booking Start Date and End Date Both Required."))
        date_from = pytz.utc.localize(datetime.strptime(vals.get('start_date', self.start_date), DEFAULT_SERVER_DATETIME_FORMAT)).astimezone(tz)
        date_to = pytz.utc.localize(datetime.strptime(vals.get('end_date', self.end_date), DEFAULT_SERVER_DATETIME_FORMAT)).astimezone(tz)
        start_time = date_from.time()
        end_time = date_to.time()
        if start_time < time(7, 00) or end_time > time(19, 00):
            raise UserError(_("Appointment Booking Only Valid Within 7AM-7PM A day."))
        x = super(sb_appointment_calender, self).write(vals)
        return x

    def sb_appointment_reminder(self):
        from datetime import datetime
        tomorrow = datetime.today() + timedelta(days=1)
        appointments = self.env['sb.appointment_calender'].search(
                [('start_date', '>=', tomorrow.strftime("%Y-%m-%d 00:00:00")), ('start_date', '<=', tomorrow.strftime("%Y-%m-%d 12:59:59"))])
        template = self.env['mail.template'].search([('name', '=', 'Appointment Reminder Template')], limit=1)
        for a in appointments:
            if template:
                mail_send = template.send_mail(a.id)
                print (mail_send)


class sb_sales_channel(models.Model):
    _name = "sb.sales_channel"

    name = fields.Char(string="Name")


class account_invoice(models.Model):
    _inherit = "account.invoice"

    name_to_make = fields.Char(string="Name To Make")
    nit = fields.Char(string="NIT")
    address = fields.Text(string="Address")
    sales_channel = fields.Many2one('sb.sales_channel', string="Sales Channel")

    @api.onchange('partner_id', 'nit', 'name_to_make', 'address', 'date_invoice')
    def onchange_customer_partner_id(self):
        self.nit = self.partner_id.nit
        self.name_to_make = self.partner_id.name_to_invoice
        self.address = self.partner_id.billing_address
        self.date_invoice = datetime.today()


class sb_medicines(models.Model):
    _name = "sb.medicines"

    name = fields.Char(string="Medicine", required=True)
    indications = fields.Char(string='Indications', required=True)
    presentation = fields.Char(string='Presentation')
    concentration = fields.Char(string='Concentration')
