# -*- coding: utf-8 -*-
{
    'name': 'Sales Order Approvals',
    'version': '18.0.1.0.0',
    'category': 'Sales',
    'summary': 'Two-level approval workflow for sale orders with amount-based routing',
    'description': """
Sales Order Approval Workflow
=============================

This module implements a comprehensive two-level approval system for sale orders, ensuring proper authorization before sales commitments are confirmed.

Key Features
------------
* **Configurable Approval Threshold**: Set a minimum amount that triggers dual validation
* **Two-Level Authorization**: Sales Manager review followed by Costing Manager validation for high-value orders
* **Conditional Routing**: Orders below threshold confirm after Sales Manager approval; amounts above threshold require additional Costing approval
* **Strict Enforcement**: Direct confirmation is blocked when approval workflow is enabled
* **Role-Based Access**: Leverages standard Sales Manager group and introduces dedicated Sale Cost Validator group

Workflow Logic
--------------
1. **Draft State**: User clicks "Request Approval" (Confirm button hidden)
2. **Sales Manager Approval**: Order moves to "Waiting Sales Manager Approval"
   - If amount ≤ threshold: Confirms immediately upon approval
   - If amount > threshold: Routes to "Waiting Costing Approval"
3. **Costing Approval**: Required for high-value orders before final confirmation
4. **Rejection**: Returns order to Draft state at any approval stage

Configuration
-------------
* Enable workflow via Sales Configuration Settings
* Define minimum amount threshold for costing approval
* Assign users to "Sale Cost Validator" group for second-level authorization

Security
--------
* Only Sales Managers can approve first level
* Only Cost Validators can approve high-value orders
* Unauthorized users receive validation errors with clear instructions
* Workflow enforced at API level preventing backend bypass
    """,
    'author': 'Code Experts IT Solutions',
    'website': 'https://www.code-experts.co',
    'depends': ['base', 'sale', 'sales_team'],
    'data': [
        'security/security.xml',
        'views/res_config_settings_views.xml',
        'views/sale_order_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': 'LGPL-3',
    'images': [
        'static/description/banner.gif',
    ],
}