from odoo import models, fields, api

class Partner(models.Model):
    _inherit = 'res.partner'
    # Define a selection field for reward levels
    reward_level = fields.Selection([
        ('argent', 'Argent'),
        ('or', 'Or'),
        ('platine', 'Platine')],
        string="Niveau de récompense")

    # Define a function to open a window displaying associated travel records
    def get_travel(self):
        self.ensure_one()
        return {
            'type': 'ir.actions.act_window',
            'name': 'Travels',
            'view_mode': 'tree,form',
            'res_model': 'travel.travel',
            'domain': [('contact_id', '=', self.id)],
            'context': "{'create': True}"
        }

    # Define a computed field to calculate the number of associated travel records
    travel_count = fields.Integer(compute='_compute_count', string="Nombre de Voyages")
    travel_ids = fields.One2many('travel.travel', 'contact_id', string="Voyages")

    # Define a dependency function for the computed travel_count field
    @api.depends('travel_ids', 'travel_ids.montant')  # Add travel_ids.montant as a dependency
    def _compute_count(self):
        for record in self:
            record.travel_count = len(record.travel_ids)


    # Define a dependency function for the reward_level field
    @api.depends('travel_ids', 'travel_ids.montant')
    def _compute_reward_level(self):
        for partner in self:
            total_spent = sum(partner.travel_ids.mapped('montant'))
            partner.reward_level = self._get_reward_level(total_spent)
    # Define an onchange function for travel_ids and travel_ids.montant fields
    @api.onchange('travel_ids', 'travel_ids.montant')
    def _onchange_travel_montant(self):
        for partner in self:
            total_spent = 0
            for travel in partner.travel_ids:
                total_spent += travel.montant
            partner.reward_level = self._get_reward_level(total_spent)
            print(f"Reward Level Updated: {partner.reward_level}")  # Add this line for debugging

    # Define a model function to calculate the reward level based on total_spent
    @api.model
    def _get_reward_level(self, total_spent):
        if total_spent > 50000:
            return 'or'
        elif total_spent > 30000:
            return 'argent'
        elif total_spent > 10000:
            return 'platine'
        else:
            return False
