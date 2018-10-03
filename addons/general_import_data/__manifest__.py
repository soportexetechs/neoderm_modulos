# -*- coding: utf-8 -*-
{
    "name": "Import Data",
    "summary": "Import data from Excel",
    "version": "10.0.1.0.0",
    "category": "import",
    "website": "http://www.laxicon.in",
    "author": "Laxicon",
    "depends": ['account'],
    "data": [
        'wizard/import_menu.xml',
        'wizard/partner_import_wiz.xml',
        'wizard/tax_import_wiz.xml',
        'wizard/payment_import_wiz.xml',
        'wizard/product_import_wiz.xml',
        'wizard/purchase_bill_import_wiz.xml',
        'wizard/sale_invoice_import_wiz.xml',
        # 'wizard/import_all_data.xml',
    ],
    'sequence': 1,
    'installable': True,
    'auto_install': False,
    'application': True,
}
