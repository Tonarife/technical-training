from odoo import fields, models

class EstatePropertyTag(models.Model):
    _name = "estate.property.tag"
    _description = "Estate property tag"
    _order = "name desc"

    name = fields.Char(required=True)

    _sql_constraints = [
            ('check_unique_tag', 'UNIQUE(name)', 'Tag must be unique.')
        ]