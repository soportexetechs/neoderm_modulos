# -*- coding: utf-8 -*-
import xlrd
import base64
from odoo import models, fields, api, _, exceptions
from odoo.exceptions import UserError


class ProductDataImport(models.TransientModel):
    _name = 'product.data.import'

    xls_file = fields.Binary('File')

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
                for product in final_data_product:
                    self.env['product.template'].create(product)
