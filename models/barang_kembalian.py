from odoo import fields, api
from odoo.models import Model
from odoo.exceptions import ValidationError


class BarangKembalian(Model):
    _name = "aset.barang_kembalian"
    _description = "Barang sewaan yang telah dikembalikan."

    item = fields.Many2many("aset.barang", string="Barang", required=True)
    rental = fields.Many2many(
        "aset.penyewaan", string="Penyewaan", required=True)
    return_ = fields.Many2many(
        "aset.pengembalian", string="Pengembalian", required=True)
    qty = fields.Integer(string="Kuantitas", default=1, required=True)

    @api.model
    def create(self, vals_list):

        item_return = super().create(vals_list)

        item = item_return.item
        rented_item_qty = item_return.rental.count_rented_item(item)
        returned_item_qty = item_return.rental.count_returned_item(item)
        return_qty = item_return.qty

        if returned_item_qty > rented_item_qty:
            raise ValidationError(
                "Kuantitas pengembalian melebihi kuantitas penyewaan.\n"
                f"Kuantitas disewa              : {rented_item_qty}\n"
                f"Kuantitas telah dikembalikan  : {returned_item_qty - return_qty}\n"
                f"Sisa barang belum dikembalikan: {rented_item_qty - returned_item_qty + return_qty}\n"
                f"Kuantitas pengembalian        : {return_qty}\n"
            )

        item.qty += item_return.qty

        item_return.check_rental_status()

        return item_return

    def check_rental_status(self):
        rental = self.rental

        rented_items = rental.count_rented_items()
        returned_items = rental.count_returned_items()
        fully_returned = True

        for (id, qty) in rented_items.items():
            if returned_items[id] != qty:
                fully_returned = False
                break

        if fully_returned:
            self.rental.status = "1"
