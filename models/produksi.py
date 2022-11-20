from odoo import fields, api
from odoo.models import Model
from odoo.exceptions import ValidationError

class Produksi(Model):
    _name = "aset.produksi"
    _description = "Perantara barang produksi."

    item = fields.Many2one("aset.barang", required=True)
    qty = fields.Integer(string="Kuantitas Produksi", required=True, default=0)

    @api.model
    def create(self, vals_list):

        production = super().create(vals_list)

        if production.qty <= 0:
            raise ValidationError(
                "Kuantitas produksi harus lebih besar dari 0.")

        production.item.qty += production.qty

        return production
