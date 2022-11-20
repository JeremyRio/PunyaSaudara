from odoo import fields, api
from odoo.models import Model
from odoo.exceptions import ValidationError


class BarangSewaan(Model):
    _name = "aset.barang_sewaan"
    _description = "Barang perusahaan yang disewakan."

    item = fields.Many2many("aset.barang", string="Barang", required=True)
    rental = fields.Many2many(
        "aset.penyewaan", string="Penyewaan", required=True)
    qty = fields.Integer(string="Kuantitas", default=1, required=True)

    @api.model
    def create(self, vals_list):

        item_rental = super().create(vals_list)

        try:
            item_rental.item.qty
        except:
            raise ValidationError(
                "Tidak bisa memilih lebih dari 1 barang.")

        try:
            item_rental.rental.client
        except:
            raise ValidationError(
                "Tidak bisa memilih lebih dari 1 penyewaan.")

        if item_rental.qty > item_rental.item.qty:
            raise ValidationError(
                "Kuantitas penyewaan melebihi kuantitas stok.")

        item_rental.item.qty -= item_rental.qty

        return item_rental

    @api.constrains('item')
    def _check_item(self):
        for record in self:
            if len(record.item) != 1:
                raise ValidationError(
                    "Record barang sewaan harus memiliki tepat 1 barang.")
