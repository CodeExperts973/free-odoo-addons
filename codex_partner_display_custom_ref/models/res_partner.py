from odoo import models, api


class ResPartner(models.Model):
    _inherit = 'res.partner'

    @api.depends('ref', 'name')  # We depend on 'ref' so it updates instantly if changed
    def _compute_display_name(self):
        # 1. Call super first to let Odoo calculate the standard name
        # (e.g., "Company Name, Contact Name")
        super()._compute_display_name()

        # 2. Iterate and prepend the reference if it exists
        for partner in self:
            if partner.ref:
                # This matches the product format: [REF] Name
                partner.display_name = f"[{partner.ref}] {partner.display_name}"