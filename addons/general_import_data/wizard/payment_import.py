# -*- coding: utf-8 -*-
import xlrd
import base64
from odoo import models, fields, api, _, exceptions
import datetime


class PaymentDataImport(models.TransientModel):
    _name = 'payment.data.import'

    xls_file = fields.Binary('File')

    @api.multi
    def import_data_payment(self):
        if not self.xls_file:
            raise exceptions.UserError(_('Please Select Excel file'))
        wb = xlrd.open_workbook(file_contents=base64.decodestring(self.xls_file))
        for sheet in wb.sheets():
            if sheet.name == 'payment':
                obj_account_payment = self.env['account.payment']
                obj_account_account = self.env['account.invoice']
                obj_account_journal = self.env['account.journal']
                # final_data_payment = []
                for row in range(sheet.nrows):
                    if row != 0:
                        amount = sheet.cell(row, 0).value
                        journal = sheet.cell(row, 1).value
                        payment_date = datetime.datetime(*xlrd.xldate_as_tuple(sheet.cell(row, 2).value, wb.datemode))
                        memo = sheet.cell(row, 3).value
                        invoice_number = sheet.cell(row, 4).value
                        invoice_id = obj_account_account.search([('number', 'like', invoice_number)], limit=1)
                        if invoice_id:
                            new_journal = journal.split(" ")[0]
                            journal_id = obj_account_journal.search([('name', 'like', new_journal)])
                            payment = obj_account_payment
                            payment_id = payment.new()
                            payment_id.state = "draft"
                            payment_id.partner_id = invoice_id.partner_id.id
                            payment_id.amount = amount
                            payment_id._onchange_amount()
                            payment_id.payment_date = payment_date
                            payment_id.communication = memo
                            payment_id.invoice_ids = [(6, 0, [invoice_id.id])]
                            payment_id.journal_id = journal_id.id
                            if invoice_id.type == "out_invoice":
                                method = self.env['account.payment.method'].search([('payment_type', '=', 'inbound')], limit=1)
                                payment_id.partner_type = "customer"
                                payment_id.payment_type = "inbound"
                                payment_id.payment_method_id = method.id
                            elif invoice_id.type == "in_invoice":
                                method = self.env['account.payment.method'].search([('payment_type', '=', 'outbound')], limit=1)
                                payment_id.partner_type = "supplier"
                                payment_id.payment_type = "outbound"
                                payment_id.payment_method_id = method.id
                            payment_id._onchange_payment_type()
                            payment = payment | payment_id
                            payment.action_validate_invoice_payment()

