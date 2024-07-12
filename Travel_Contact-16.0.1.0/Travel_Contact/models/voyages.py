from odoo import models, fields, api


class Voyage(models.Model):
    _name = 'travel.travel'
    _description = 'Modèle Voyage'

    # Define fields for the travel record
    name = fields.Char(string="Nom du voyage", related='list_voyages_id.name', store=True)
    depart = fields.Char(string="Lieux de Depart", related='list_voyages_id.depart', store=True)
    destination = fields.Char(string="Destination", related='list_voyages_id.destination', store=True)
    time_depart = fields.Datetime(string="Date de départ", related='list_voyages_id.time_depart', store=True)

    # Updated field: The number of reserved places by contacts
    nb_place = fields.Integer(string="Nombre de places réservées", required=True)
    montant = fields.Float(string="Montant", required=True)  # Add the montant field

    @api.onchange('montant')
    def _onchange_montant(self):
        if self.contact_id:
            # Call the _compute_reward_level function of the associated res.partner record
            self.contact_id._compute_reward_level()

    # Define an onchange function for the montant field
    @api.onchange('nb_place')
    def _onchange_nb_place(self):
        for record in self:
            if record.list_voyages_id:
                total_reserved_places = sum(record.list_voyages_id.travel_ids.mapped('nb_place'))
                record.list_voyages_id.reserved_nb_place = total_reserved_places

    # Define a many2one relationship to the res.partner model
    contact_id = fields.Many2one('res.partner', string="Contact")

    # Define a computed field for the status
    status = fields.Selection([
        ('empty', 'Empty'),
        ('full', 'Full')],
        string="Statut",
        related='list_voyages_id.status', store=True)

    # Add a related field to get the list.voyages record
    list_voyages_id = fields.Many2one('list.voyages', string="Liste des Voyages")
