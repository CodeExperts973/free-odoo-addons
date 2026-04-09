from odoo import fields, models
from odoo.exceptions import ValidationError


class AccountMove(models.Model):
    _inherit = 'account.move'

    state = fields.Selection(selection_add=[
        ('waiting_support_approval', 'Waiting Support Approval'),
        ('waiting_accounting_approval', 'Waiting Accounting Approval'),
        ('waiting_general_approval', 'Waiting General Approval'),
        ('waiting_payment_validator_1', 'Waiting Payment Validator 1'),
        ('waiting_payment_validator_2', 'Waiting Payment Validator 2'),
    ], ondelete={
        'waiting_support_approval': 'set default',
        'waiting_accounting_approval': 'set default',
        'waiting_general_approval': 'set default',
        'waiting_payment_validator_1': 'set default',
        'waiting_payment_validator_2': 'set default'
    })

    def action_post(self):
        for move in self:
            if move.move_type not in ('out_invoice', 'in_invoice', 'out_refund', 'in_refund'):
                continue
            if move.state == 'draft' and self.env['ir.config_parameter'].sudo().get_param('codex_invoice_approvals.invoice_approval'):
                raise ValidationError("Please request approval first.")
        return super(AccountMove, self).action_post()

    def action_request_approval(self):
        for move in self:
            if move.move_type not in ('out_invoice', 'in_invoice', 'out_refund', 'in_refund'):
                continue
            if move.move_type == 'in_invoice':
                move.state = 'waiting_payment_validator_1'
                continue  # Use continue to skip the threshold logic below
            threshold = float(self.env['ir.config_parameter'].sudo().get_param('codex_invoice_approvals.invoice_threshold_amount') or 1000.0)
            if move.amount_total < threshold:
                if move.move_type in 'out_invoice':
                    move.state = 'waiting_support_approval'
                elif move.move_type in ('out_refund', 'in_refund'):
                    move.state = 'waiting_accounting_approval'
            else:
                move.state = 'waiting_general_approval'

    def action_approve(self):
        # Refactored for clarity and to fix the recursive loop
        for move in self:
            if move.move_type not in ('out_invoice', 'in_invoice', 'out_refund', 'in_refund'):
                continue

            if move.state == 'waiting_payment_validator_1':
                if not self.env.user.has_group('codex_invoice_approvals.group_invoice_payment_validator_1'):
                    raise ValidationError("You are not authorized to approve this. Contact Payment Validator 1.")
                move.state = "waiting_payment_validator_2"
                continue

            is_final_approval = False
            if move.state == 'waiting_support_approval':
                if not self.env.user.has_group('codex_invoice_approvals.group_invoice_support_approver'):
                    raise ValidationError("You are not authorized. Contact the Support Service Manager.")
                is_final_approval = True
            elif move.state == 'waiting_accounting_approval':
                if not self.env.user.has_group('codex_invoice_approvals.group_invoice_accounting_approver'):
                    raise ValidationError("You are not authorized. Contact the Accounting Manager.")
                is_final_approval = True
            elif move.state == 'waiting_general_approval':
                if not self.env.user.has_group('codex_invoice_approvals.group_invoice_general_approver'):
                    raise ValidationError("You are not authorized. Contact the General Manager.")
                is_final_approval = True
            elif move.state == 'waiting_payment_validator_2':
                if not self.env.user.has_group('codex_invoice_approvals.group_invoice_payment_validator_2'):
                    raise ValidationError("You are not authorized. Contact Payment Validator 2.")
                is_final_approval = True

            if is_final_approval:
                super(AccountMove, move).action_post()
            else:
                raise ValidationError("This document is not in a valid state for approval.")

    def action_reject(self):
        self.write({'state': 'draft'})