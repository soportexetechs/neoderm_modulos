# -*- coding: utf-8 -*-
import xlrd
import base64
from odoo import models, fields, api, _, exceptions
from odoo.exceptions import UserError
import datetime


class GetAllDataImport(models.TransientModel):
    _name = 'get.all.data.import'

    xls_file = fields.Binary('File')

    @api.multi
    def import_data_partner(self):
        if not self.xls_file:
            raise exceptions.UserError(_('Please Select Excel file'))
        wb = xlrd.open_workbook(file_contents=base64.decodestring(self.xls_file))
        final_data_customer = []
        for sheet in wb.sheets():
            if sheet.name == 'Partner':
                final_data_customer = []
                # set data in list
                for row in range(sheet.nrows):
                    if row != 0:
                        state_name = sheet.cell(row, 4).value
                        state_id = False
                        if state_name:
                            self._cr.execute("""SELECT id FROM res_country_state WHERE name = '%s'""" % (state_name))
                            state_name = self._cr.fetchone()
                            state_id = state_name and state_name[0] or False
                        partner_name = sheet.cell(row, 0).value
                        nit = sheet.cell(row, 8).value
                        if not partner_name and not nit:
                            msg = 'Partner not Avaiable ' \
                                    'Partner name  %s and NIT %s !\n ' % (partner_name, nit)
                            raise UserError(_('Data Not Available !\n' + msg))
                        self._cr.execute("""SELECT id FROM res_partner where name like '%s'  AND vat = '%s'""" % (partner_name, nit))
                        partner_name = self._cr.fetchone()
                        partner = partner_name and partner_name[0] or False
                        customer = False
                        if sheet.cell(row, 6).value and sheet.cell(row, 6).value == 1:
                            customer = True
                        supplier = False
                        if sheet.cell(row, 7).value and sheet.cell(row, 7).value == 1:
                            supplier = True
                        if not partner:
                            data = {
                                'name': sheet.cell(row, 0).value,
                                'street': sheet.cell(row, 1).value,
                                'street2': sheet.cell(row, 2).value,
                                'city': sheet.cell(row, 3).value,
                                'state_id': state_id or False,
                                'zip': sheet.cell(row, 5).value,
                                'customer': customer,
                                'supplier': supplier,
                                'vat': sheet.cell(row, 8).value,
                                'phone': sheet.cell(row, 9).value,
                                'mobile': sheet.cell(row, 10).value,
                                'email': sheet.cell(row, 11).value,
                                'company_type': sheet.cell(row, 12).value
                            }
                            final_data_customer.append(data)
                # create final data for parner
                for partner in final_data_customer:
                    self.env['res.partner'].create(partner)
                # create all partner

    @api.multi
    def import_data_tax(self):
        if not self.xls_file:
            raise exceptions.UserError(_('Please Select Excel file'))
        wb = xlrd.open_workbook(file_contents=base64.decodestring(self.xls_file))
        final_data_tax = []
        for sheet in wb.sheets():
            if sheet.name == 'Tax':
                final_data_tax = []
                # set data in list
                for row in range(sheet.nrows):
                    if row != 0:
                        account_name = sheet.cell(row, 4).value
                        self._cr.execute("""SELECT id from account_account WHERE name = '%s'""" % (account_name))
                        d_tax_id = self._cr.fetchone()
                        d_tax = d_tax_id and d_tax_id[0] or False

                        account_name = sheet.cell(row, 5).value
                        self._cr.execute("""SELECT id from account_account WHERE name = '%s'""" % (account_name))
                        c_tax_id = self._cr.fetchone()
                        c_tax = c_tax_id and c_tax_id[0] or False

                        # tax find
                        tax_name = sheet.cell(row, 0).value
                        scope = sheet.cell(row, 1).value
                        if not tax_name and not scope:
                            msg = 'Tax not Avaiable ' \
                                    'Tax name  %s !\n ' % (tax_name)
                            raise UserError(_('Please Check Tax !\n' + msg))
                        self._cr.execute("""SELECT id from account_tax WHERE name = '%s'""" % (sheet.cell(row, 0).value))
                        tax_id = self._cr.fetchone()
                        tax = tax_id and tax_id[0] or False
                        if not tax:
                            tax_dict = {
                                'name': sheet.cell(row, 0).value,
                                'type_tax_use': sheet.cell(row, 1).value,
                                'amount_type': sheet.cell(row, 2).value,
                                'amount': sheet.cell(row, 3).value,
                                'account_id': d_tax or False,
                                'refund_account_id': c_tax or False,
                                'description': sheet.cell(row, 6).value,
                                'price_include': sheet.cell(row, 7).value,
                            }
                            final_data_tax.append(tax_dict)
                # create tax from list
                for tax in final_data_tax:
                    self.env['account.tax'].create(tax)

    @api.multi
    def import_data_product(self):
        if not self.xls_file:
            raise exceptions.UserError(_('Please Select Excel file'))
        wb = xlrd.open_workbook(file_contents=base64.decodestring(self.xls_file))
        final_data_product = []
        for sheet in wb.sheets():
            if sheet.name == 'Product':
                final_data_product = []
                # set data in list
                for row in range(sheet.nrows):
                    if row != 0:
                        self._cr.execute("""SELECT id from product_category WHERE name = '%s'""" % (sheet.cell(row, 3).value))
                        product_categ_id = self._cr.fetchone()
                        product_categ = product_categ_id and product_categ_id[0] or False
                        s_tax_name = sheet.cell(row, 6).value,
                        self._cr.execute("""SELECT id from account_tax WHERE name = '%s'""" % (s_tax_name))
                        s_tax_id = self._cr.fetchone()
                        sale_tax = s_tax_id and s_tax_id[0] or False
                        if s_tax_name and not sale_tax:
                            msg = 'Sale TAX not Avaiable ' \
                                    'Tax name  %s !\n ' % (s_tax_name)
                            raise UserError(_('Data Not Available !\n' + msg))
                        v_tax_name = sheet.cell(row, 8).value,
                        self._cr.execute("""SELECT id from account_tax WHERE name = '%s'""" % (v_tax_name))
                        p_tax_id = self._cr.fetchone()
                        purchase_tax = p_tax_id and p_tax_id[0] or False
                        if v_tax_name and not purchase_tax:
                            msg = 'Vendor TAX not Avaiable ' \
                                    'Tax name  %s !\n ' % (s_tax_name)
                            raise UserError(_('Data Not Available !\n' + msg))
                        sale_ok = False
                        if sheet.cell(row, 10).value and sheet.cell(row, 10).value == 1:
                            sale_ok = True
                        purchase_ok = False
                        if sheet.cell(row, 11).value and sheet.cell(row, 11).value == 1:
                            purchase_ok = True
                        name = sheet.cell(row, 0).value
                        default_code = str(sheet.cell(row, 2).value)
                        product_domain = []
                        if name:
                            product_domain.append(('name', 'ilike', name))
                        if default_code:
                            product_domain.append(('default_code', 'ilike', default_code))
                        product_id = False
                        if product_domain:
                            product_id = self.env['product.template'].search(product_domain, limit=1)
                        #     product_data = self._cr.fetchone()
                        #     product_id = product_data and product_data[0] or False
                        if not product_id:
                            data = {
                                'name': name,
                                'type': sheet.cell(row, 1).value,
                                'default_code': default_code,
                                'lst_price': sheet.cell(row, 4).value,
                                'standard_price': sheet.cell(row, 5).value,
                                'sale_ok': sale_ok,
                                'purchase_ok': purchase_ok,
                                'categ_id': product_categ or 1,
                                'taxes_id': [(6, 0, [sale_tax])],
                                'supplier_taxes_id': [(6, 0, [purchase_tax])],
                               }
                            final_data_product.append(data)

                        # self.env['product.template'].create(data)
                # create product from list
                # cnt = 0
                for product in final_data_product:
                    # if cnt == 50:
                    #     break
                    self.env['product.template'].create(product)
                    # cnt += 1

    @api.multi
    def import_data_invoice(self):
        if not self.xls_file:
            raise exceptions.UserError(_('Please Select Excel file'))
        wb = xlrd.open_workbook(file_contents=base64.decodestring(self.xls_file))
        for sheet in wb.sheets():
            if sheet.name == 'Invoice':
                invoice_list = []
                invoice_val = []
                for row in range(sheet.nrows):
                    if row != 0:
                        obj_product = self.env['product.template']
                        in_type = sheet.cell(row, 1).value
                        partner_name = sheet.cell(row, 2).value.strip()
                        nit = sheet.cell(row, 3).value
                        domain = []
                        if partner_name:
                            domain.append(('name', 'ilike', partner_name))
                        if nit:
                            domain.append(('vat', '=', nit))
                        err_msg = ''
                        if in_type == "out_invoice":
                            domain.append(('customer', '=', True))
                            err_msg = "Customer"
                        elif in_type == "in_invoice":
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
                        # if in_type == "out_invoice":
                        #     invoice_data.update({'x_studio_field_ngXF8': extra_id.id})
                        # elif in_type == "in_invoice":
                        #     invoice_data.update({'x_studio_field_45LWE': extra_id.id})
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
                                    # if in_type == "out_invoice":
                                    #     invoice_line_ids.update({'x_studio_field_ngXF8': final_data.get('x_studio_field_ngXF8')})
                                    # elif in_type == "in_invoice":
                                    #     invoice_line_ids.update({'x_studio_field_45LWE': final_data.get('x_studio_field_45LWE')})
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
                    }
                    obj_account_inv = self.env['account.invoice']
                    invoice_id = obj_account_inv.create(order_data)
                    if invoice_id:
                        # invoice_id.create_from_import(inv_data.get('lines'), inv_data.get('number'))
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
                            # if line.get('x_studio_field_ngXF8', False):
                            #     invoice_line.x_studio_field_ngXF8 = line.get('x_studio_field_ngXF8')
                            # if line.get('x_studio_field_45LWE', False):
                            #     invoice_line.x_studio_field_45LWE = line.get('x_studio_field_45LWE')
                            invoice_id.invoice_line_ids = invoice_id.invoice_line_ids | invoice_line
                        invoice_id._onchange_invoice_line_ids()
                        invoice_id.action_invoice_open()
                        invoice_id.write({'number': inv_data.get('number')})

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

    # @api.multi
    # def import_data(self):
    #     if not self.xls_file:
    #         raise exceptions.UserError(_('Please Select Excel file'))
    #     wb = xlrd.open_workbook(file_contents=base64.decodestring(self.xls_file))
    #     final_data_customer = []
    #     final_data_tax = []
    #     final_data_product = []
    #     for sheet in wb.sheets():
    #         if sheet.name == 'Partner':
    #             final_data_customer = []
    #             # set data in list
    #             for row in range(sheet.nrows):
    #                 if row != 0:
    #                     state_name = sheet.cell(row, 4).value
    #                     state_id = False
    #                     if state_name:
    #                         self._cr.execute("""SELECT id FROM res_country_state WHERE name = '%s'""" % (state_name))
    #                         state_name = self._cr.fetchone()
    #                         state_id = state_name and state_name[0] or False
    #                     partner_name = sheet.cell(row, 0).value
    #                     nit = sheet.cell(row, 8).value
    #                     if not partner_name and not nit:
    #                         msg = 'Partner not Avaiable ' \
    #                                 'Partner name  %s and NIT %s !\n ' % (partner_name, nit)
    #                         raise UserError(_('Data Not Available !\n' + msg))
    #                     self._cr.execute("""SELECT id FROM res_partner where name like '%s'  AND vat = '%s'""" % (partner_name, nit))
    #                     partner_name = self._cr.fetchone()
    #                     partner = partner_name and partner_name[0] or False
    #                     customer = False
    #                     if sheet.cell(row, 6).value and sheet.cell(row, 6).value == 1:
    #                         customer = True
    #                     supplier = False
    #                     if sheet.cell(row, 7).value and sheet.cell(row, 7).value == 1:
    #                         supplier = True
    #                     if not partner:
    #                         partner_data = {
    #                             'name': sheet.cell(row, 0).value,
    #                             'street': sheet.cell(row, 1).value,
    #                             'street2': sheet.cell(row, 2).value,
    #                             'city': sheet.cell(row, 3).value,
    #                             'state_id': state_id or False,
    #                             'zip': sheet.cell(row, 5).value,
    #                             'customer': customer,
    #                             'supplier': supplier,
    #                             'vat': sheet.cell(row, 8).value,
    #                             'phone': sheet.cell(row, 9).value,
    #                             'mobile': sheet.cell(row, 10).value,
    #                             'email': sheet.cell(row, 11).value,
    #                             'company_type': sheet.cell(row, 12).value
    #                         }
    #                         final_data_customer.append(partner_data)
    #             # create final data for parner
    #             for partner in final_data_customer:
    #                 self.env['res.partner'].create(partner)
    #             # create all partner
    #         if sheet.name == 'Tax':
    #             final_data_tax = []
    #             # set data in list
    #             for row in range(sheet.nrows):
    #                 if row != 0:
    #                     account_name = sheet.cell(row, 4).value
    #                     self._cr.execute("""SELECT id from account_account WHERE name = '%s'""" % (account_name))
    #                     d_tax_id = self._cr.fetchone()
    #                     d_tax = d_tax_id and d_tax_id[0] or False

    #                     account_name = sheet.cell(row, 5).value
    #                     self._cr.execute("""SELECT id from account_account WHERE name = '%s'""" % (account_name))
    #                     c_tax_id = self._cr.fetchone()
    #                     c_tax = c_tax_id and c_tax_id[0] or False

    #                     # tax find
    #                     tax_name = sheet.cell(row, 0).value
    #                     scope = sheet.cell(row, 1).value
    #                     if not tax_name and not scope:
    #                         msg = 'Tax not Avaiable ' \
    #                                 'Tax name  %s !\n ' % (tax_name)
    #                         raise UserError(_('Please Check Tax !\n' + msg))
    #                     self._cr.execute("""SELECT id from account_tax WHERE name = '%s'""" % (sheet.cell(row, 0).value))
    #                     tax_id = self._cr.fetchone()
    #                     tax = tax_id and tax_id[0] or False
    #                     if not tax:
    #                         tax_dict = {
    #                             'name': sheet.cell(row, 0).value,
    #                             'type_tax_use': sheet.cell(row, 1).value,
    #                             'amount_type': sheet.cell(row, 2).value,
    #                             'amount': sheet.cell(row, 3).value,
    #                             'account_id': d_tax or False,
    #                             'refund_account_id': c_tax or False,
    #                             'description': sheet.cell(row, 6).value,
    #                             'price_include': sheet.cell(row, 7).value,
    #                         }
    #                         final_data_tax.append(tax_dict)
    #             # create tax from list
    #             for tax in final_data_tax:
    #                 self.env['account.tax'].create(tax)
    #         if sheet.name == 'Product':
    #             final_data_product = []
    #             # set data in list
    #             for row in range(sheet.nrows):
    #                 if row != 0:
    #                     self._cr.execute("""SELECT id from product_category WHERE name = '%s'""" % (sheet.cell(row, 3).value))
    #                     product_categ_id = self._cr.fetchone()
    #                     product_categ = product_categ_id and product_categ_id[0] or False
    #                     s_tax_name = sheet.cell(row, 6).value,
    #                     self._cr.execute("""SELECT id from account_tax WHERE name = '%s'""" % (s_tax_name))
    #                     s_tax_id = self._cr.fetchone()
    #                     sale_tax = s_tax_id and s_tax_id[0] or False
    #                     if s_tax_name and not sale_tax:
    #                         msg = 'Sale TAX not Avaiable ' \
    #                                 'Tax name  %s !\n ' % (s_tax_name)
    #                         raise UserError(_('Data Not Available !\n' + msg))
    #                     v_tax_name = sheet.cell(row, 8).value,
    #                     self._cr.execute("""SELECT id from account_tax WHERE name = '%s'""" % (v_tax_name))
    #                     p_tax_id = self._cr.fetchone()
    #                     purchase_tax = p_tax_id and p_tax_id[0] or False
    #                     if v_tax_name and not purchase_tax:
    #                         msg = 'Vendor TAX not Avaiable ' \
    #                                 'Tax name  %s !\n ' % (s_tax_name)
    #                         raise UserError(_('Data Not Available !\n' + msg))
    #                     sale_ok = False
    #                     if sheet.cell(row, 10).value and sheet.cell(row, 10).value == 1:
    #                         sale_ok = True
    #                     purchase_ok = False
    #                     if sheet.cell(row, 11).value and sheet.cell(row, 11).value == 1:
    #                         purchase_ok = True
    #                     name = sheet.cell(row, 0).value
    #                     default_code = str(sheet.cell(row, 2).value)
    #                     product_domain = []
    #                     if name:
    #                         product_domain.append(('name', 'ilike', name))
    #                     if default_code:
    #                         product_domain.append(('default_code', 'ilike', default_code))
    #                     product_id = False
    #                     if product_domain:
    #                         product_id = self.env['product.template'].search(product_domain, limit=1)
    #                     #     product_data = self._cr.fetchone()
    #                     #     product_id = product_data and product_data[0] or False
    #                     if not product_id:
    #                         product_data = {
    #                             'name': name,
    #                             'type': sheet.cell(row, 1).value,
    #                             'default_code': default_code,
    #                             'lst_price': sheet.cell(row, 4).value,
    #                             'standard_price': sheet.cell(row, 5).value,
    #                             'sale_ok': sale_ok,
    #                             'purchase_ok': purchase_ok,
    #                             'categ_id': product_categ or 1,
    #                             'taxes_id': [(6, 0, [sale_tax])],
    #                             'supplier_taxes_id': [(6, 0, [purchase_tax])],
    #                            }
    #                         final_data_product.append(product_data)

    #                     # self.env['product.template'].create(data)
    #             # create product from list
    #             cnt = 0
    #             for product in final_data_product:
    #                 if cnt == 50:
    #                     break
    #                 self.env['product.template'].create(product)
    #                 cnt += 1
    #         if sheet.name == 'Invoice':
    #             invoice_list = []
    #             invoice_val = []
    #             for row in range(sheet.nrows):
    #                 if row != 0:
    #                     obj_product = self.env['product.template']
    #                     in_type = sheet.cell(row, 1).value
    #                     partner_name = sheet.cell(row, 2).value.strip()
    #                     nit = sheet.cell(row, 3).value
    #                     domain = []
    #                     if partner_name:
    #                         domain.append(('name', 'ilike', partner_name))
    #                     if nit:
    #                         domain.append(('vat', '=', nit))
    #                     err_msg = ''
    #                     if in_type == "out_invoice":
    #                         domain.append(('customer', '=', True))
    #                         err_msg = "Customer"
    #                     elif in_type == "in_invoice":
    #                         domain.append(('supplier', '=', True))
    #                         err_msg = "Supplier"
    #                     partner_id = self.env['res.partner'].search(domain, limit=1)
    #                     if not partner_id:
    #                         msg = '%s not Avaiable ' \
    #                                 'Partner name  %s and NIT %s !\n ' % (err_msg, partner_name, nit)
    #                         raise UserError(_('Data Not Available !\n' + msg))
    #                     product_name = sheet.cell(row, 6).value
    #                     product_id = obj_product.search([('name', 'ilike', product_name)], limit=1)
    #                     if not product_id:
    #                         msg = 'Product not Avaiable ' \
    #                                 'Product name  _(%s) !\n ' % (product_name)
    #                         raise UserError(_('Data Not Available !\n' + msg))
    #                     tax_name = sheet.cell(row, 10).value
    #                     self._cr.execute("""SELECT id from account_tax where name  like '%s'""" % (tax_name))
    #                     tax_id = [data[0] for data in self._cr.fetchall()]
    #                     if tax_name and not tax_id:
    #                         msg = 'Tax not Avaiable ' \
    #                                 'Tax name  %s and !\n ' % (tax_name)
    #                         raise UserError(_('Data Not Available !\n' + msg))
    #                     extra_field = sheet.cell(row, 11).value
    #                     extra_id = False
    #                     if extra_field:
    #                         extra_id = self.env['x_centro_de_costo'].search([('x_name', 'ilike', extra_field)], limit=1)
    #                     int_date = datetime.datetime(*xlrd.xldate_as_tuple(sheet.cell(row, 4).value, wb.datemode))
    #                     invoice_data = {
    #                         'number': sheet.cell(row, 0).value,
    #                         'type': in_type,
    #                         'partner_id': partner_id.id,
    #                         'date_invoice': int_date,
    #                         'origin': sheet.cell(row, 5).value,
    #                         'product_id': product_id.id,
    #                         'quantity': sheet.cell(row, 7).value,
    #                         'price_unit': sheet.cell(row, 8).value,
    #                         'tax': tax_id,
    #                     }
    #                     if in_type == "out_invoice":
    #                         invoice_data.update({'x_studio_field_ngXF8': extra_id.id})
    #                     elif in_type == "in_invoice":
    #                         invoice_data.update({'x_studio_field_45LWE': extra_id.id})
    #                     invoice_list.append(invoice_data)
    #             if invoice_list:
    #                 invoice_dict = {}
    #                 for key in invoice_list:
    #                     in_type = key['type']
    #                     if key['number'] not in invoice_dict.keys():
    #                         data = {
    #                             'number': key['number'],
    #                             'type': key['type'],
    #                             'partner_id': key['partner_id'],
    #                             'date_invoice': key['date_invoice'],
    #                             'origin': key['origin'],
    #                         }
    #                         invoice_dict.update({key['number']: data})
    #                     for key in invoice_dict:
    #                         lst = []
    #                         for final_data in invoice_list:
    #                             if key == final_data['number']:
    #                                 invoice_line_ids = {
    #                                     'product_id': final_data.get('product_id'),
    #                                     'quantity': final_data.get('quantity'),
    #                                     'price_unit': final_data.get('price_unit'),
    #                                     'tax': final_data.get('tax'),
    #                                      }
    #                                 if in_type == "out_invoice":
    #                                     invoice_line_ids.update({'x_studio_field_ngXF8': final_data.get('x_studio_field_ngXF8')})
    #                                 elif in_type == "in_invoice":
    #                                     invoice_line_ids.update({'x_studio_field_45LWE': final_data.get('x_studio_field_45LWE')})
    #                                 lst.append(invoice_line_ids)
    #                             if lst and invoice_dict.get(key):
    #                                 invoice_dict.get(key).update({'lines': lst})
    #                 for d in invoice_dict.values():
    #                     invoice_val.append(d)
    #             for inv_data in invoice_val:
    #                 order_data = {
    #                     'partner_id': inv_data.get('partner_id'),
    #                     'date_invoice': inv_data.get('date_invoice'),
    #                     'type': inv_data.get('type'),
    #                     'number': inv_data.get('number'),
    #                 }
    #                 obj_account_inv = self.env['account.invoice']
    #                 invoice_id = obj_account_inv.create(order_data)
    #                 if invoice_id:
    #                     # invoice_id.create_from_import(inv_data.get('lines'), inv_data.get('number'))
    #                     invoice_lines = invoice_id.invoice_line_ids
    #                     for line in inv_data.get('lines'):
    #                         invoice_line = invoice_lines.new()
    #                         invoice_line.invoice_id = invoice_id.id
    #                         invoice_line.product_id = line.get('product_id')
    #                         invoice_line._onchange_product_id()
    #                         invoice_line.quantity = line.get('quantity')
    #                         invoice_line.price_unit = line.get('price_unit')
    #                         invoice_line.invoice_line_tax_ids = []
    #                         invoice_line.invoice_line_tax_ids = [[6, 0, line.get('tax')]]
    #                         if line.get('x_studio_field_ngXF8', False):
    #                             invoice_line.x_studio_field_ngXF8 = line.get('x_studio_field_ngXF8')
    #                         if line.get('x_studio_field_45LWE', False):
    #                             invoice_line.x_studio_field_45LWE = line.get('x_studio_field_45LWE')
    #                         invoice_id.invoice_line_ids = invoice_id.invoice_line_ids | invoice_line
    #                     invoice_id._onchange_invoice_line_ids()
    #                     invoice_id.action_invoice_open()
    #                     invoice_id.write({'number': inv_data.get('number')})
