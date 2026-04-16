# -*- coding: utf-8 -*-
{
    'name': 'Invoice Approvals',
    'version': '18.0.1.0.0',
    'category': 'Accounting',
    'summary': 'Multi-level approval workflow for invoices and refunds with amount-based routing',
    'description': """
Invoice and Refund Approval Workflow
====================================

This module implements a comprehensive approval system for customer invoices, vendor bills, and credit notes/refunds before they can be posted.

Key Features
------------
* **Multi-State Approval Workflow**: Extends account move states with dedicated approval stages
* **Amount-Based Routing**: Automatically routes documents based on configurable threshold amount
* **Vendor Bill Two-Step Validation**: Special workflow for vendor bills requiring validation from Payment Validator 1 then Payment Validator 2
* **Role-Based Permissions**: Five distinct approval groups with specific authorization levels
* **Configurable Threshold**: Settings to define amount limit for senior approval requirements

Approval Workflow Logic
-----------------------
* **Draft State**: Users must click "Request Approval" instead of "Post"
* **Vendor Bills (in_invoice)**: Route to Payment Validator 1 → Payment Validator 2 → Posted
* **Customer Invoices below threshold**: Route to Support Approver → Posted  
* **Refunds below threshold**: Route to Accounting Approver → Posted
* **Invoices/Refunds above threshold**: Route to General Approver → Posted
* **Rejection**: Returns document to draft state for correction

Security Groups
---------------
* Invoice Support Approver: Can approve invoices below threshold amount
* Invoice Accounting Approver: Can approve refunds below threshold amount  
* Invoice General Approver: Can approve invoices/refunds at or above threshold amount
* Bill Payment Validator 1: Can validate vendor bills and forward to Validator 2
* Bill Payment Validator 2: Can perform final validation and approve vendor bills

Configuration
-------------
* Enable/disable invoice approval requirement via Accounting Settings
* Configure threshold amount that determines approval routing
* Settings accessible under Invoicing/Accounting Configuration

    """,
    'author': 'Code Experts IT Solutions',
    'website': 'https://www.code-experts.co',
    'depends': ['base', 'account'],
    'data': [
        'security/security.xml',
        'views/res_config_settings_views.xml',
        'views/account_move_views.xml',
    ],
    'images': [
        'static/description/banner.gif',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
}