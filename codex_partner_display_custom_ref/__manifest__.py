# -*- coding: utf-8 -*-
{
    'name': 'Partner Reference in Display Name',
    'version': '18.0.1.0.0',
    'category': 'Sales',
    'summary': 'Display partner internal reference code [REF] prefix before name across all views',
    'description': """
Partner Reference Display Format
================================

Automatically prepends the partner's Internal Reference code to their display name across the entire Odoo system, following the same format used for products ([REF] Name).

Features
--------
* **Automatic Formatting**: Displays contacts as `[REF] Partner Name` when internal reference is set
* **System-Wide Application**: Works in list views, form views, kanban, Many2one dropdowns, and search results
* **Backward Compatible**: Partners without references display normally without brackets
* **Zero Configuration**: Uses existing `ref` field on res.partner—no setup required
* **Search Compatible**: Users can search by reference code or name in relational fields

Use Cases
---------
* Quickly identify customers by account numbers in Sales Orders
* Distinguish suppliers by vendor codes in Purchase workflows  
* Visual differentiation between duplicate company names using unique references
* Faster data entry when codes are shorter than full company names

Technical
---------
* Inherits and extends `res.partner._compute_display_name`
* Non-intrusive compute method—calls super() to preserve standard logic
* Updates instantly when reference code is modified
* No database schema changes or additional fields created
    """,
    'author': 'Code Experts IT Solutions',
    'website': 'http://www.codeexperts.com',
    'depends': ['base', 'contacts'],
    'data': [],
    'images': [
        'static/description/banner.gif',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
    'license': "OPL-1",
}