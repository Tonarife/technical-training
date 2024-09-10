from odoo import api, fields, models
from datetime import date
from dateutil.relativedelta import relativedelta

class EstateProperty(models.Model):
    _name = "estate.property"
    _description = "Estate property model"
    _order = "id desc"

    name = fields.Char(required=True)
    description = fields.Text()
    active = fields.Boolean(default=True)
    state = fields.Selection(
        string='State',
        selection=[('new', 'New'), ('received', 'Offer Received'), ('accepted', 'Offer Accepted'), ('sold', 'Sold'), ('canceled', 'Canceled')],
        help="State", required=True, copy=False, default='new')
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
    estate_property_id = fields.Many2one("estate.property.type", string="type")
    user_id = fields.Many2one('res.users', string='Salesperson', index=True, tracking=True, default=lambda self: self.env.user)
    buyer = fields.Many2one("res.partner", string="Buyer", copy=False)
    tags_ids = fields.Many2many("estate.property.tag", string="Tags")
    offer_ids = fields.One2many("estate.property.offer","property_id", string="Offers")
    total_area = fields.Float(compute="_compute_total")
    best_price = fields.Float(compute="_compute_best")

    _sql_constraints = [
        ('check_selling_price', 'CHECK(selling_price > 0)',
         'Selling price must be a positive number.'),
        ('check_expected_price', 'CHECK(expected_price > 0)', 'Selling price must be a positive number.')
    ]

    @api.depends("living_area", "garden_area")
    def _compute_total(self):
        for record in self:
            record.total_area = record.living_area + record.garden_area

    @api.depends("offer_ids.price")
    def _compute_best(self):
        for record in self:
            if record.offer_ids.price > 0:
                record.best_price = max(record.offer_ids.mapped('price'))
            else:
                record.best_price = 0

    @api.onchange("garden")
    def _onchange_partner_id(self):
        if self.garden: 
            self.garden_area = 10
            self.garden_orientation = 'north'
        else:
            self.garden_area = 0
            self.garden_orientation = ''

    def action_sold(self):
        for record in self:
            if record.state == "canceled":
                return {
                'effect': {
                    'fadeout': 'slow',
                    'message': "No se puede vender",
                    'type': 'rainbow_man',
                }
            }
            record.state = "sold"
        return True

    def action_cancel(self):
        for record in self:
            if record.state == "sold":
                return {
                'effect': {
                    'fadeout': 'slow',
                    'message': "No se puede cancelar",
                    'type': 'rainbow_man',
                }
            }
            record.state = "canceled"
        return True