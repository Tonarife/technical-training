from odoo import fields, models
from datetime import date
from dateutil.relativedelta import relativedelta

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate property model"

    name = fields.Char(required=True)
    description = fields.Text()
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string='State',
        selection=[('new', 'New'), ('received', 'Offer Received'), ('accepted', 'Offer Accepted'), ('sold', 'Sold'), ('canceled', 'Canceled')],
        help="Garden orientation", required=True, copy=False, default='new')
    postcode = fields.Char()
    date_availability = fields.Date(copy=False, default=(date.today() + relativedelta(months=+3)))
    expected_price = fields.Float(required=True)
    selling_price = fields.Float(readonly=True, copy=False)
    bedrooms = fields.Integer(default=2)
    living_area = fields.Integer()
    facades = fields.Integer()
    garage = fields.Boolean()
    garden = fields.Boolean()
    garden_area = fields.Integer()
    garden_orientation = fields.Selection(
        string='Orientation',
        selection=[('north', 'North'), ('south', 'South'), ('east', 'East'), ('west', 'West')],
        help="Garden orientation")
    estate_property_id = fields.Many2one("estate.property.type.name", string="type")
    user_id = fields.Many2one('res.users', string='Salesperson', index=True, tracking=True, default=lambda self: self.env.user)
    buyer = fields.Many2one("res.partner", string="Buyer", copy=False)