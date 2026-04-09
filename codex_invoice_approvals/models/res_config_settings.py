from odoo import api, fields, models


class ResConfigSettings(models.TransientModel):
    _inherit = 'res.config.settings'

    invoice_approval = fields.Boolean(
        string="Invoice Approval",
        help="Enable this option to require approvals for invoices and refunds."
    )
    invoice_threshold_amount = fields.Monetary(
        string="Threshold Amount for Senior Approval",
        help="Specify the amount below which the junior approver can approve. "
             "Invoices/Refunds equal to or above this amount require General Manager approval."
    )

    @api.model
    def get_values(self):
        res = super(ResConfigSettings, self).get_values()
        res['invoice_approval'] = bool(self.env['ir.config_parameter'].sudo().get_param(
            "codex_invoice_approvals.invoice_approval", default=False))
        res['invoice_threshold_amount'] = float(self.env['ir.config_parameter'].sudo().get_param(
            "codex_invoice_approvals.invoice_threshold_amount", default=1000.0))
        return res

    def set_values(self):
        self.env['ir.config_parameter'].sudo().set_param(
            "codex_invoice_approvals.invoice_approval",
            self.invoice_approval)
        self.env['ir.config_parameter'].sudo().set_param(
            "codex_invoice_approvals.invoice_threshold_amount",
            self.invoice_threshold_amount or 1000.0)
        super(ResConfigSettings, self).set_values()