# -*- coding: utf-8 -*-
import xlrd
import base64
from odoo import models, fields, api, _, exceptions
from odoo.exceptions import UserError
import datetime


class PurchaseBillDataImport(models.TransientModel):
    _name = 'purchase.bill.data.import'

    xls_file = fields.Binary('File')
    journal_id = fields.Many2one('account.journal', string='Journal', required=True, domain="[('type', 'in', ['purchase'])]")

    @api.multi
    def import_data_bill(self):
        if not self.xls_file:
            raise exceptions.UserError(_('Please Select Excel file'))
        wb = xlrd.open_workbook(file_contents=base64.decodestring(self.xls_file))
        for sheet in wb.sheets():
            if sheet.name == 'Invoice':
                invoice_list = []
                invoice_val = []
                for row in range(sheet.nrows):
                    if row != 0:
                        in_type = sheet.cell(row, 1).value
                        if in_type == "in_invoice":
                            obj_product = self.env['product.template']
                            partner_name = sheet.cell(row, 2).value.strip()
                            nit = sheet.cell(row, 3).value
                            domain = []
                            if partner_name:
                                domain.append(('name', 'ilike', partner_name))
                            if nit:
                                domain.append(('vat', '=', nit))
                            err_msg = ''
                            if in_type == "in_invoice":
                                domain.append(('supplier', '=', True))
                                err_msg = "Supplier"
                            partner_id = self.env['res.partner'].search(domain, limit=1)
                            if not partner_id:
                                msg = '%s not Avaiable ' \
                                        'Partner name  %s and NIT %s !\n ' % (err_msg, partner_name, nit)
                                raise UserError(_('Data Not Available !\n' + msg))
                            product_name = sheet.cell(row, 6).value
                            product_id = obj_product.search([('name', 'ilike', product_name)], limit=1)
                            if not product_id:
                                msg = 'Product not Avaiable ' \
                                        'Product name  _(%s) !\n ' % (product_name)
                                raise UserError(_('Data Not Available !\n' + msg))
                            # tax_name = sheet.cell(row, 10).value
                            # self._cr.execute("""SELECT id from account_tax where name  like '%s'""" % (tax_name))
                            # tax_id = [data[0] for data in self._cr.fetchall()]
                            tax_data = sheet.cell(row, 10).value
                            tax_ids = []
                            if tax_data:
                                tax_list = tax_data.split(",")
                                tax_ids = self.env['account.tax'].search([('name', 'in', tax_list)])
                                if tax_list and not tax_ids:
                                    msg = 'Tax not Avaiable '
                                    raise UserError(_('Data Not Available !\n' + msg))
                                tax_ids = tax_ids.ids
                            extra_field = sheet.cell(row, 11).value
                            extra_id = False
                            if extra_field:
                                # extra_id = self.env['x_centro_de_costo'].search([('x_name', 'ilike', extra_field)], limit=1)
                                extra_id = self.env['account.analytic.account'].search([('name', 'ilike', extra_field)], limit=1).id
                            int_date = datetime.datetime(*xlrd.xldate_as_tuple(sheet.cell(row, 4).value, wb.datemode))
                            due_date = datetime.datetime(*xlrd.xldate_as_tuple(sheet.cell(row, 12).value, wb.datemode))
                            invoice_data = {
                                'number': sheet.cell(row, 0).value,
                                'type': in_type,
                                'partner_id': partner_id.id,
                                'date_invoice': int_date,
                                'date_due': due_date,
                                'origin': sheet.cell(row, 5).value,
                                'product_id': product_id.id,
                                'quantity': sheet.cell(row, 7).value,
                                'price_unit': sheet.cell(row, 8).value,
                                'tax': tax_ids,
                                'account_analytic_id': extra_id
                            }
                            invoice_list.append(invoice_data)
                if invoice_list:
                    invoice_dict = {}
                    for key in invoice_list:
                        in_type = key['type']
                        if key['number'] not in invoice_dict.keys():
                            data = {
                                'number': key['number'],
                                'type': key['type'],
                                'partner_id': key['partner_id'],
                                'date_invoice': key['date_invoice'],
                                'origin': key['origin'],
                                'date_due': key['date_due'],
                            }
                            invoice_dict.update({key['number']: data})
                        for key in invoice_dict:
                            lst = []
                            for final_data in invoice_list:
                                if key == final_data['number']:
                                    invoice_line_ids = {
                                        'product_id': final_data.get('product_id'),
                                        'quantity': final_data.get('quantity'),
                                        'price_unit': final_data.get('price_unit'),
                                        'tax': final_data.get('tax'),
                                        'account_analytic_id': final_data.get('account_analytic_id'),
                                         }
                                    lst.append(invoice_line_ids)
                                if lst and invoice_dict.get(key):
                                    invoice_dict.get(key).update({'lines': lst})
                    for d in invoice_dict.values():
                        invoice_val.append(d)
                for inv_data in invoice_val:
                    order_data = {
                        'partner_id': inv_data.get('partner_id'),
                        'date_invoice': inv_data.get('date_invoice'),
                        'type': inv_data.get('type'),
                        'number': inv_data.get('number'),
                        'date_due': inv_data.get('date_due'),
                        'journal_id': self.journal_id.id,
                    }
                    obj_account_inv = self.env['account.invoice']
                    invoice_id = obj_account_inv.create(order_data)
                    if invoice_id:
                        invoice_lines = invoice_id.invoice_line_ids
                        for line in inv_data.get('lines'):
                            invoice_line = invoice_lines.new()
                            invoice_line.invoice_id = invoice_id.id
                            invoice_line.product_id = line.get('product_id')
                            invoice_line._onchange_product_id()
                            invoice_line.quantity = line.get('quantity')
                            invoice_line.price_unit = line.get('price_unit')
                            invoice_line.account_analytic_id = line.get('account_analytic_id')
                            invoice_line.invoice_line_tax_ids = []
                            invoice_line.invoice_line_tax_ids = [[6, 0, line.get('tax')]]
                            invoice_id.invoice_line_ids = invoice_id.invoice_line_ids | invoice_line
                        invoice_id._onchange_invoice_line_ids()
                        invoice_id.action_invoice_open()
                        invoice_id.write({'number': inv_data.get('number')})
