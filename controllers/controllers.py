# -*- coding: utf-8 -*-
from odoo import http


class Asset(http.Controller):

    @http.route('/asset/', auth='public', website=True)
    def index(self, **kw):
        return http.request.render('PunyaSaudara.index', {
        })

    @http.route('/asset/items/', auth='user', website=True)
    def items(self, **kw):
        items = http.request.env["aset.barang"]
        return http.request.render('PunyaSaudara.barang', {
            "items": items.search([])
        })

    @http.route('/asset/items/new', auth='user', website=True, methods=["POST"])
    def items_new_handle(self, **kw):
        try:
            params = http.request.get_http_params()
            http.request.env["aset.barang"].create(
                {"name": params["name"], "qty": 0})
            http.request.cr.commit()
            return http.request.make_response("", headers=[("Location", "/asset/items")], status=303)
        except Exception as e:
            return http.request.make_response("", headers=[("Location", f"/asset/items/new?err={e}")], status=303)

    @http.route('/asset/items/new', auth='user', website=True, methods=["GET"])
    def items_new(self, **kw):
        return http.request.render('PunyaSaudara.barang_new', {
        })

    @http.route('/asset/items/produce', auth='user', website=True, methods=["GET"])
    def items_produce(self, **kw):
        items = http.request.env["aset.barang"]
        return http.request.render('PunyaSaudara.barang_produce', {
            "items": items.search([])
        })

    @http.route('/asset/items/produce', auth='user', website=True, methods=["POST"])
    def items_produce_handle(self, **kw):
        try:
            params = http.request.get_http_params()
            record = http.request.env["aset.barang"].browse(
                [int(params["id"])])
            record.qty += int(params["qty"])
            http.request.cr.commit()
            return http.request.make_response("", headers=[("Location", "/asset/items")], status=303)
        except Exception as e:
            return http.request.make_response("", headers=[("Location", f"/asset/items/produce?err={e}")], status=303)

    # @http.route('/asset/rentals/', auth='user', website=True)
    # def rentals(self, **kw):
    #     rentals = http.request.env["aset.penyewaan"]
    #     return http.request.render('PunyaSaudara.penyewaan', {
    #         "rentals": rentals.search([])
    #     })

    # @http.route('/asset/rentals/<year>/<month>', auth='user', website=True)
    # def rentals(self, year, month, **kw):
    #     rental_items = http.request.env["aset.barang_sewaan"]
    #     return http.request.render('PunyaSaudara.penyewaan', {
    #         "rental_items": rental_items.search([("rental.month", "=", int(month)), ("rental.year", "=", int(year))])
    #     })

    @http.route('/asset/rentals/', auth='user', website=True)
    def rentals(self, **kw):
        rental_items = http.request.env["aset.barang_sewaan"]
        return http.request.render('PunyaSaudara.penyewaan', {
            "rental_items": rental_items.search([])
        })

    @http.route('/asset/rentals/new', auth='user', website=True, methods=["GET"])
    def rentals_new(self, **kw):
        rentals = http.request.env["aset.penyewaan"]
        items = http.request.env["aset.barang"]
        return http.request.render('PunyaSaudara.penyewaan_new', {
            "rentals": rentals.search([]),
            "items": items.search([]),
        })

    @http.route('/asset/rentals/new', auth='user', website=True, methods=["POST"])
    def rentals_new_item_handle(self, **kw):
        try:
            params = http.request.get_http_params()
            rental = http.request.env["aset.penyewaan"].browse(
                [int(params["rental-id"])])
            item = http.request.env["aset.barang"].browse(
                [int(params["item-id"])])
            http.request.env["aset.barang_sewaan"].create(
                {"item": item.id, "rental": rental.id, "qty": params["qty"]})
            http.request.cr.commit()
            return http.request.make_response("", headers=[("Location", "/asset/rentals")], status=303)
        except Exception as e:
            return http.request.make_response("", headers=[("Location", f"/asset/rentals/new?err={e}")], status=303)

    @http.route('/asset/rentals/new-rental', auth='user', website=True, methods=["POST"])
    def rentals_new_handle(self, **kw):
        try:
            params = http.request.get_http_params()
            date_component = params["date"].split("/")
            date_component.reverse()
            date_component[1], date_component[2] = date_component[2], date_component[1]
            date = "-".join(date_component)
            http.request.env["aset.penyewaan"].create(
                {"client": params["client"],
                 "rental_date": date,
                 "duration": params["duration"]})
            http.request.cr.commit()
            return http.request.make_response("", headers=[("Location", "/asset/rentals/new")], status=303)
        except Exception as e:
            return http.request.make_response("", headers=[("Location", f"/asset/rentals/new?err={e}")], status=303)

    # @http.route('/asset/returns/<year>/<month>', auth='user', website=True)
    # def returns(self, **kw):
    #     items = http.request.env["aset.barang"]
    #     print(items)
    #     print(items.search([]))
    #     return http.request.render('PunyaSaudara.barang', {
    #         "items": items.search([])
    #     })

    @http.route('/asset/returns/', auth='user', website=True)
    def returns(self, **kw):
        return_items = http.request.env["aset.barang_kembalian"]
        return http.request.render('PunyaSaudara.pengembalian', {
            "return_items": return_items.search([])
        })

    @http.route('/asset/returns/new', auth='user', website=True, methods=["GET"])
    def returns_new(self, **kw):
        returns = http.request.env["aset.pengembalian"]
        rentals = http.request.env["aset.penyewaan"]
        items = http.request.env["aset.barang"]
        return http.request.render('PunyaSaudara.pengembalian_new', {
            "returns": returns.search([]),
            "rentals": rentals.search([]),
            "items": items.search([])
        })

    @http.route('/asset/returns/new', auth='user', website=True, methods=["POST"])
    def returns_new_item_handle(self, **kw):
        try:
            params = http.request.get_http_params()
            rental = http.request.env["aset.penyewaan"].browse(
                [int(params["rental-id"])])
            item = http.request.env["aset.barang"].browse(
                [int(params["item-id"])])
            return_ = http.request.env["aset.pengembalian"].browse(
                [int(params["return-id"])])
            http.request.env["aset.barang_kembalian"].create(
                {"item": item.id, "rental": rental.id, "return_": return_.id, "qty": params["qty"]})
            http.request.cr.commit()
            return http.request.make_response("", headers=[("Location", "/asset/returns")], status=303)
        except Exception as e:
            return http.request.make_response("", headers=[("Location", f"/asset/returns/new?err={e}")], status=303)

    @http.route('/asset/returns/new-return', auth='user', website=True, methods=["POST"])
    def returns_new_handle(self, **kw):
        try:
            params = http.request.get_http_params()
            date_component = params["date"].split("/")
            date_component.reverse()
            date_component[1], date_component[2] = date_component[2], date_component[1]
            date = "-".join(date_component)
            http.request.env["aset.pengembalian"].create(
                {"return_date": date})
            http.request.cr.commit()
            return http.request.make_response("", headers=[("Location", "/asset/returns/new")], status=303)
        except Exception as e:
            return http.request.make_response("", headers=[("Location", f"/asset/returns/new?err={e}")], status=303)

    @http.route('/asset/items/report', auth='user', website=True)
    def items_report(self, **kw):
        items = http.request.env["aset.barang"]
        print(items)
        print(items.search([]))
        return http.request.render('PunyaSaudara.barang', {
            "items": items.search([])
        })

    @http.route('/asset/rentals/report', auth='user', website=True)
    def rentals_report(self, **kw):
        items = http.request.env["aset.barang"]
        print(items)
        print(items.search([]))
        return http.request.render('PunyaSaudara.barang', {
            "items": items.search([])
        })

    @http.route('/asset/returns/report', auth='user', website=True)
    def returns_report(self, **kw):
        items = http.request.env["aset.barang"]
        print(items)
        print(items.search([]))
        return http.request.render('PunyaSaudara.barang', {
            "items": items.search([])
        })
