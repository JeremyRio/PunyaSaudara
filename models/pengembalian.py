from odoo import fields
from odoo.models import Model


class Pengembalian(Model):
    _name = "aset.pengembalian"
    _description = "Pengembalian barang yang telah dilakukan oleh klien."

    return_date = fields.Date(string="Tanggal Pengembalian", required=True)
    items = fields.One2many(
        "aset.barang_kembalian", required=True, inverse_name="return_")

    def date_string(self):
        year = self.return_date.strftime("%Y")
        month_index = self.return_date.strftime("%m")
        date = self.return_date.strftime("%d")

        months = ["Januari", "Februari", "Maret", "April", "Mei", "Juni",
                  "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
        month = months[int(month_index) - 1]

        return f"{date} {month} {year}"
