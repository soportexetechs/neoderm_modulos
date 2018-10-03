# -*- coding: utf-8 -*-
import xlrd
import base64
from odoo import models, fields, api, _, exceptions
from odoo.exceptions import UserError


class TaxDataImport(models.TransientModel):
    _name = 'tax.data.import'

    xls_file = fields.Binary('File')

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