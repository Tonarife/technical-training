from odoo import api, fields, models
from datetime import date
from dateutil.relativedelta import relativedelta
from odoo.exceptions import UserError, ValidationError
from odoo.tools.float_utils import float_compare, float_is_zero, float_round

class EstatePropertyOffer(models.Model):
    _name = "estate.property.offer"
    _description = "Estate property offer"
    _order = "price desc"

    price = fields.Float()
    status = fields.Selection(
        string='Status',
        selection=[('accepted', 'Accepted'), ('refused', 'Refused')],
        help="Status", copy=False)
    partner_id = fields.Many2one("res.partner", required=True)
    property_id = fields.Many2one("estate.property", required=True)
    validity = fields.Integer(default=7)
    date_deadline = fields.Date(compute="_compute_deadline")

    _sql_constraints = [
        ('check_price', 'CHECK(price > 0)', 'Price must be a positive number.')
    ]

    @api.depends("validity")
    def _compute_deadline(self):
        for record in self:
            if record.create_date is not False:
                record.date_deadline = record.create_date + relativedelta(days=+record.validity)
            else:
                record.date_deadline = date.today() + relativedelta(days=+record.validity)

    @api.constrains('selling_price')
    def check_selling_price(self):
        for price in self:
            if float_is_zero(price.price,2) == False:
                if (100 * price.property_id.expected_price/price.price) < float(90.00):
                    raise ValidationError('The selling price is lower than 90% of expected price')

    def _inverse_deadline(self):
        for record in self:
            record.date_deadline = record.deadline - record.validity

    def action_confirm(self):
        for record in self:           
            record.status = "accepted"
            record.property_id.buyer = record.partner_id
            record.property_id.selling_price = record.price
        return True

    def action_refuse(self):
        for record in self:
            record.status = "refused"
        return True