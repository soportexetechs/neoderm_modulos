# -*- encoding: UTF-8 -*-
from odoo import api, models, _, fields, exceptions


class AccountInvoice(models.Model):
    _inherit = 'account.invoice'

    @api.multi
    def create_from_import(self, data, number):
        print (data)
        invoice_lines = self.invoice_line_ids
        for line in data:
            invoice_line = invoice_lines.new()
            invoice_line.invoice_id = self.id
            invoice_line.product_id = line.get('product_id')
            invoice_line._onchange_product_id()
            invoice_line.quantity = line.get('quantity')
            invoice_line.price_unit = line.get('price_unit')
            invoice_line.invoice_line_tax_ids = []
            invoice_line.invoice_line_tax_ids = [[6, 0, line.get('tax')]]
            if line.get('x_studio_field_ngXF8', False):
                invoice_line.x_studio_field_ngXF8 = line.get('x_studio_field_ngXF8')
            if line.get('x_studio_field_45LWE', False):
                invoice_line.x_studio_field_45LWE = line.get('x_studio_field_45LWE')
            self.invoice_line_ids = self.invoice_line_ids | invoice_line
        self._onchange_invoice_line_ids()
        self.action_invoice_open()
        self.write({'number': number})

# class AccountInvoiceLine(models.Model):
#     _inherit = 'account.invoice.line'

#     @api.onchange('product_id')
#     def onchange_product_id(self):
#         domain = {}
#         if not self.invoice_id:
#             return
#         part = self.invoice_id.partner_id
#         fpos = self.invoice_id.fiscal_position_id
#         company = self.invoice_id.company_id
#         currency = self.invoice_id.currency_id
#         type = self.invoice_id.type

#         if not part:
#             warning = {
#                     'title': _('Warning!'),
#                     'message': _('You must first select a partner!'),
#                 }
#             return {'warning': warning}

#         if not self.product_id:
#             if type not in ('in_invoice', 'in_refund'):
#                 self.price_unit = 0.0
#             domain['uom_id'] = []
#         else:
#             # Use the purchase uom by default
#             self.uom_id = self.product_id.uom_po_id

#             if part.lang:
#                 product = self.product_id.with_context(lang=part.lang)
#             else:
#                 product = self.product_id

#             self.name = product.partner_ref
#             account = self.get_invoice_line_account(type, product, fpos, company)
#             if account:
#                 self.account_id = account.id
#             self._set_taxes()

#             if type in ('in_invoice', 'in_refund'):
#                 if product.description_purchase:
#                     self.name += '\n' + product.description_purchase
#             else:
#                 if product.description_sale:
#                     self.name += '\n' + product.description_sale

#             if not self.uom_id or product.uom_id.category_id.id != self.uom_id.category_id.id:
#                 self.uom_id = product.uom_id.id
#             domain['uom_id'] = [('category_id', '=', product.uom_id.category_id.id)]

#             if company and currency:
#                 if company.currency_id != currency:
#                     self.price_unit = self.price_unit * currency.with_context(dict(self._context or {}, date=self.invoice_id.date_invoice)).rate

#                 if self.uom_id and self.uom_id.id != product.uom_id.id:
#                     self.price_unit = product.uom_id._compute_price(self.price_unit, self.uom_id)
#         return {'domain': domain}
