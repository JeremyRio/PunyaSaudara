from odoo import fields, api
from odoo.models import Model
from odoo.exceptions import ValidationError


class BarangSewaan(Model):
    _name = "aset.barang_sewaan"
    _description = "Barang perusahaan yang disewakan."

    item = fields.Many2one("aset.barang", string="Barang", required=True)
    rental = fields.Many2one(
        "aset.penyewaan", string="Penyewaan", required=True)
    qty = fields.Integer(string="Kuantitas", default=1, required=True)

    @api.model
    def create(self, vals_list):
        print(vals_list)

        qty = int(vals_list["qty"])
        item = self.env["aset.barang"].browse([vals_list["item"]])
        rental = self.env["aset.penyewaan"].browse([vals_list["rental"]])

        if qty > item.qty:
            raise ValidationError(
                "Kuantitas penyewaan melebihi kuantitas stok.")

        if rental.status == "1":
            raise ValidationError(
                "Penyewaan telah dikembalikan.")

        item_rental = super().create(vals_list)
        item_rental.item.qty -= item_rental.qty

        return item_rental

    @api.constrains('item')
    def _check_item(self):
        for record in self:
            if len(record.item) != 1:
                raise ValidationError(
                    "Record barang sewaan harus memiliki tepat 1 barang.")
