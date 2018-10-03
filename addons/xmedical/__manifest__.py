# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

##############################################################################
#
#    SnippetBucket, MidSized Business Application Solution
#    Copyright (C) 2013-2014 http://snippetbucket.com/. All Rights Reserved.
#    Email: snippetbucket@gmail.com, Skype: live.snippetbucket
#
#
##############################################################################
{
    'name': "Medical Clinic",
    'summary': """SnippetBucket Medical Clinic.""",
    'description': """
        Support: info@laxicon.in
        Powered by: Laxicon solution
    """,
    'depends': ['base', 'mail', 'account'],
    'author': "Laxicon",
    'website': "http://laxicon.in/",
    'category': 'medical',
    'version': '0.1',

    'data': [
            'security/medical_clinic_security.xml',
            'security/ir.model.access.csv',
            'reports/report_invoices.xml',
            'reports/report_patient_recipes.xml',
            # 'views/views.xml',
            'views/custome_css_template.xml',
            'views/appointment_mail_template.xml',
            'views/menu_view.xml',
            'views/res_partner_view.xml',
            'views/patient_detail_view.xml',
            'views/patient_appoinment_view.xml',
            'views/medical_hostory_view.xml',
            'views/insurence_list.view.xml',
            'views/time_slot_view.xml',

            ],

    'demo': [],
    'sequence': 1,
    'installable': True,
    'auto_install': False,
    'application': True,
    'images': [],
    "license": 'Other proprietary',
}
