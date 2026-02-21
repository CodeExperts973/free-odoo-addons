from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    so_approval = fields.Boolean(
        string="Sale Order Approval",
        help="Enable this option to require double validation for sale orders. "
             "When enabled, sale orders exceeding the specified minimum amount "
             "will require approval by a sales manager."
    )
    so_min_amount = fields.Monetary(
        string="Minimum Sale Order Amount",
        help="Specify the minimum amount that triggers the double validation "
             "for sale orders. Sale orders exceeding this amount will require "
             "approval by a sales manager."
    )

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res['so_approval'] = self.env['ir.config_parameter'].sudo().get_param(
            "codex_sales_approvals.so_approval", default="")
        res['so_min_amount'] = self.env['ir.config_parameter'].sudo().get_param(
            "codex_sales_approvals.so_min_amount", default="")
        return res

    @api.model
    def set_values(self):
        self.env['ir.config_parameter'].set_param(
            "codex_sales_approvals.so_approval",
            self.so_approval or '')
        self.env['ir.config_parameter'].set_param(
            "codex_sales_approvals.so_min_amount",
            self.so_min_amount or '')
        super(ResConfigSettings, self).set_values()
