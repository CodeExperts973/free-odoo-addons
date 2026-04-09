# -*- coding: utf-8 -*-
{
    'name': "Scrap Approval",
    'summary': "Manager Approval Workflow for Scrap Orders",
    'description': """
        Scrap Manager Approval Workflow
        ================================

        This module implements a multi-step approval workflow for scrap orders:

        1. **New State**: Adds "Waiting for Manager Approval" state to scrap orders
        2. **Approval Process**: 
           - Users submit scrap orders for approval
           - Managers receive notifications/activities for pending approvals
           - Managers can Approve or Reject scrap orders
           - Reset to Draft functionality is provided
        3. **Notifications**:
           - Automatic activity creation for managers
        4. **Workflow**:
           Draft → Waiting for Manager Approval → Approved/Rejected → Done/Cancelled

        Features:
        - Custom security groups for scrap approvers
        - Activity-based approval interface
        - Audit trail of approval actions
        - Configurable approval rules
    """,
    'author': 'Code Experts IT Solutions',
    'license': 'LGPL-3',
    'category': 'Inventory',
    'version': '18.0.1.0.0',
    'depends': ['stock', 'mail'],
    'data': [
        'security/security.xml',
        'views/stock_scap_views.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'support': 'hello@code-experts.co',
    'images': [
        'static/description/banner.gif',
    ],
}