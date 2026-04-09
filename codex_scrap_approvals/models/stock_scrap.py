from odoo import api, fields, models, _
from odoo.exceptions import UserError


class StockScrap(models.Model):
    _name = 'stock.scrap'
    _inherit = ['stock.scrap', 'mail.activity.mixin']

    state = fields.Selection(selection_add=[
        ('manager_approval', 'Waiting Manager Approval'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    ], ondelete={'manager_approval': 'set default',
                 'approved': 'set default',
                 'rejected': 'set default'
                 })

    approver_ids = fields.Many2many(
        'res.users',
        string='Scrap Approvers',
        compute='_compute_approver_ids',
        store=False
    )

    def _compute_approver_ids(self):
        """Get all users in the Scrap Manager Approver group"""
        approver_group = self.env.ref('codex_scrap_approvals.group_scrap_manager_approval', raise_if_not_found=False)
        if approver_group:
            approvers = approver_group.users
            for scrap in self:
                scrap.approver_ids = approvers
        else:
            for scrap in self:
                scrap.approver_ids = False

    def action_to_manager_approval(self):
        self.ensure_one()
        approver_group = self.env.ref('codex_scrap_approvals.group_scrap_manager_approval', raise_if_not_found=False)

        if not approver_group or not approver_group.users:
            raise UserError(_('No scrap approvers found. Please assign users to the "Scrap Manager Approver" group.'))

        # Change state
        self.state = 'manager_approval'

        # Prepare notification message
        body = _('Scrap Order %s requires your approval.') % self.name

        # Get all approvers' partner IDs
        approvers = approver_group.users
        partner_ids = approvers.mapped('partner_id').ids

        # Post message in the chatter
        self.message_post(
            body=body,
            partner_ids=partner_ids,
            subtype_xmlid='mail.mt_note'
        )

        # Create activity for each approver
        for user in approvers:
            if hasattr(self, 'activity_schedule'):
                print("yes----------------------------------")
                self.activity_schedule(
                    'mail.mail_activity_data_todo',
                    summary=_('Approve Scrap Order'),
                    note=_('Please review and approve scrap order: %s') % self.name,
                    user_id=user.id
                )
            else:
                print("no-----------------------------------")
                # Method 2: Create activity directly
                self.env['mail.activity'].create({
                    'activity_type_id': self.env.ref('mail.mail_activity_data_todo').id,
                    'summary': _('Approve Scrap Order'),
                    'note': _('Please review and approve scrap order: %s') % self.name,
                    'user_id': user.id,
                    'res_id': self.id,
                    'res_model_id': self.env['ir.model']._get_id('stock.scrap'),
                    'date_deadline': fields.Date.context_today(self),
                })

        return True

    def action_to_approved(self):
        self.ensure_one()
        self.state = "approved"

        # Clear all related activities when approved
        activities = self.env['mail.activity'].search([
            ('res_model', '=', 'stock.scrap'),
            ('res_id', '=', self.id),
            ('activity_type_id', '=', self.env.ref('mail.mail_activity_data_todo').id)
        ])
        if activities:
            activities.action_done()

        # Post approval message
        self.message_post(body=_('Scrap order has been approved by %s.') % self.env.user.name)

        return True

    def action_to_rejected(self):
        self.ensure_one()
        self.state = "rejected"

        # Clear all related activities when rejected
        activities = self.env['mail.activity'].search([
            ('res_model', '=', 'stock.scrap'),
            ('res_id', '=', self.id),
            ('activity_type_id', '=', self.env.ref('mail.mail_activity_data_todo').id)
        ])
        if activities:
            activities.action_done()

        # Post rejection message
        self.message_post(body=_('Scrap order has been rejected by %s.') % self.env.user.name)

        return True

    def action_reset_to_draft(self):
        self.ensure_one()
        self.state = "draft"

        # Clear any pending activities when resetting
        activities = self.env['mail.activity'].search([
            ('res_model', '=', 'stock.scrap'),
            ('res_id', '=', self.id),
            ('activity_type_id', '=', self.env.ref('mail.mail_activity_data_todo').id)
        ])
        if activities:
            activities.unlink()

        return True