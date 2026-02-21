from odoo import fields, models, _
from odoo.exceptions import ValidationError


class SaleOrder(models.Model):
    _inherit = 'sale.order'

    state = fields.Selection(selection_add=[
        ('sales_manager_approve', 'Waiting Sales Manager Approval'),
        ('costing_approve', 'Waiting Costing Approval'),
    ], ondelete={'sales_manager_approve': 'set default', 'costing_approve': 'set default'})

    def _confirmation_error_message(self):
        self.ensure_one()
        if self.state not in {'draft', 'sent', 'sales_manager_approve', 'costing_approve'}:
            return _("Some orders are not in a state requiring confirmation.")
        if any(
            not line.display_type
            and not line.is_downpayment
            and not line.product_id
            for line in self.order_line
        ):
            return _("A line on these orders missing a product, you cannot confirm it.")

        return False

    def action_confirm(self):
        if self.state == 'draft' and self.env['ir.config_parameter'].sudo().get_param('codex_sales_approvals.so_approval'):
            raise ValidationError("Please request approval first.")
        error_message = self._confirmation_error_message()
        if error_message:
            raise ValidationError(error_message)
        return super(SaleOrder, self).action_confirm()

    def action_request_manager_approval(self):
        self.state = 'sales_manager_approve'

    def action_manager_approve(self):
        if not self.env.user.has_group('sales_team.group_sale_manager'):
            raise ValidationError("You are not authorized to approve this sale order. Contact the sales manager.")
        min_amount = float(self.env['ir.config_parameter'].sudo().get_param('codex_sales_approvals.so_min_amount') or 0.0)
        if self.env['ir.config_parameter'].sudo().get_param('codex_sales_approvals.so_approval') and self.amount_total > min_amount:
            self.state = 'costing_approve'
        else:
            return self.action_confirm()

    def action_costing_approve(self):
        if not self.env.user.has_group('codex_sales_approvals.group_sale_cost_validator'):
            raise ValidationError("You are not authorized to approve this sale order. Contact the costing manager.")
        return self.action_confirm()

    def action_reject(self):
        self.state = 'draft'