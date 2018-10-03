# -*- coding: utf-8 -*-
import xlrd
import base64
from odoo import models, fields, api, _, exceptions
from odoo.exceptions import UserError


class PartnerDataImport(models.TransientModel):
    _name = 'partner.data.import'

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
