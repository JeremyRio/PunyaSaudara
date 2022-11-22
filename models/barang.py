from odoo import fields, api
from odoo.models import Model


class Barang(Model):
    _name = "aset.barang"
    _description = "Aset barang milik perusahaan."

    name = fields.Char(string="Nama Barang", required=True)
    qty = fields.Integer(string="Kuantitas", required=True, default=0)

    def count_unreturned(self):
        rentals = self.env['aset.penyewaan']
        unreturned = 0
        for rental in rentals.search([]):
            unreturned += rental.count_rented_item(
                self) - rental.count_returned_item(self)

        return unreturned
