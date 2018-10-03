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
