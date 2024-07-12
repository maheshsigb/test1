from odoo import models, fields, api


class ListVoyages(models.Model):
    _name = 'list.voyages'
    _description = 'Liste des Voyages'

    name = fields.Char(string="Nom du voyage", required=True)
    depart = fields.Char(string="Lieux de Depart", required=True)
    destination = fields.Char(string="Destination", required=True)
    time_depart = fields.Datetime(string="Date de départ", required=True)

    # Total number of empty places
    total_nb_place = fields.Integer(string="Nombre total de places", required=True)

    # Updated field: Number of reserved places by contacts
    reserved_nb_place = fields.Integer(string="Nombre de places réservées", compute='_compute_reserved_nb_place',
                                       store=True)

    # Define a computed field for the status
    status = fields.Selection([
        ('empty', 'Empty'),
        ('full', 'Full')],
        string="Statut",
        compute='_compute_status', store=True)

    # One2many relationship to the travel.travel model to store reserved places data
    travel_ids = fields.One2many('travel.travel', 'list_voyages_id', string="Voyages")

    @api.depends('travel_ids', 'travel_ids.nb_place')
    def _compute_reserved_nb_place(self):
        for record in self:
            total_reserved_places = sum(record.travel_ids.mapped('nb_place'))
            record.reserved_nb_place = total_reserved_places

    @api.depends('total_nb_place', 'reserved_nb_place')
    def _compute_status(self):
        for record in self:
            if record.reserved_nb_place >= record.total_nb_place:
                record.status = 'full'
            else:
                record.status = 'empty'
