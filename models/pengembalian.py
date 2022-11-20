from odoo import fields
from odoo.models import Model


class Pengembalian(Model):
    _name = "aset.pengembalian"
    _description = "Pengembalian barang yang telah dilakukan oleh klien."

    return_date = fields.Date(string="Tanggal Pengembalian", required=True)
