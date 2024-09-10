from odoo import fields, models

class EstatePropertyType(models.Model):
    _name = "estate.property.type"
    _description = "Estate property type"
    _order = "name desc"

    name = fields.Char(required=True)
    property_ids = fields.One2many("estate.property","estate_property_id", string="Types")
    sequence = fields.Integer()