from odoo import fields, api
from odoo.models import Model


class Barang(Model):
    _name = "aset.barang"
    _description = "Aset barang milik perusahaan."

    name = fields.Char(string="Nama Barang", required=True)
    qty = fields.Integer(string="Kuantitas", required=True, default=0)
