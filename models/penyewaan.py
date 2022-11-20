from odoo import fields, api
from odoo.models import Model


class Penyewaan(Model):
    _name = "aset.penyewaan"
    _description = "Penyewaan yang telah dilayani oleh perusahaan."

    client = fields.Char(string="Klien", required=True)
    durations = fields.Integer(string="Durasi (hari)", required=True)
    rental_date = fields.Date(string="Tanggal Sewa", required=True)
    status = fields.Selection(string="Status", required=True, selection=[
        ("0", "Belum Dikembalikan"), ("1", "Dikembalikan")
    ])

    items = fields.Many2many(
        "aset.barang_sewaan", required=True)

    returned_items = fields.Many2many("aset.barang_kembalian", required=True)

    def __str__(self) -> str:
        return super().__str__()

    def count_rented_items(self):

        rented_items = {}

        for item_rental in self.items:
            id = item_rental.item.id
            qty = item_rental.qty

            if id not in rented_items:
                rented_items[id] = 0
            rented_items[id] += qty

        return rented_items

    def count_returned_items(self):
        returned_items = {}

        for item_return in self.returned_items:
            id = item_return.item.id
            qty = item_return.qty

            if id not in returned_items:
                returned_items[id] = 0
            returned_items[id] += qty

        return returned_items

    def count_rented_item(self, item) -> int:
        qty = 0

        for item_rental in self.items:
            if item_rental.item.id == item.id:
                qty += item_rental.qty

        return qty

    def count_returned_item(self, item) -> int:
        qty = 0

        for item_return in self.returned_items:
            if item_return.item.id == item.id:
                qty += item_return.qty

        return qty

    def write(self, vals):
        return super().write(vals)
