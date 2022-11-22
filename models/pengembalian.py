from odoo import fields, api
from odoo.models import Model


class Pengembalian(Model):
    _name = "aset.pengembalian"
    _description = "Pengembalian barang yang telah dilakukan oleh klien."

    return_date = fields.Date(string="Tanggal Pengembalian", required=True)
    items = fields.One2many(
        "aset.barang_kembalian", required=True, inverse_name="return_")
    month = fields.Integer(compute="_get_month", store=True)
    year = fields.Integer(compute="_get_year", store=True)

    def date_string(self):
        year = self.return_date.strftime("%Y")
        month_index = self.return_date.strftime("%m")
        date = self.return_date.strftime("%d")

        months = ["Januari", "Februari", "Maret", "April", "Mei", "Juni",
                  "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
        month = months[int(month_index) - 1]

        return f"{date} {month} {year}"

    @api.depends("return_date")
    def _get_month(self):
        for record in self:
            record.month = record.return_date.strftime("%m")

    @api.depends("return_date")
    def _get_year(self):
        for record in self:
            record.year = record.return_date.strftime("%Y")

    def count_items(self):
        returned_items = {}

        for item_return in self.items:
            id = item_return.item.id
            qty = item_return.qty

            if id not in returned_items:
                returned_items[id] = 0
            returned_items[id] += qty

        return returned_items
