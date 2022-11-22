# -*- coding: utf-8 -*-
from odoo import http
from datetime import datetime

MONTHS = ["Januari", "Februari", "Maret", "April", "Mei", "Juni",
          "Juli", "Agustus", "September", "Oktober", "November", "Desember"]
ESTABLISHMENT_YEAR = 2021


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
        return http.request.render('PunyaSaudara.barang_report', {
            "items": items.search([])
        })

    @http.route('/asset/rentals/report', auth='user', website=True)
    def rentals_report_prompt(self, **kw):
        this_year = datetime.now().year
        years = [y for y in range(ESTABLISHMENT_YEAR, this_year + 1)]
        return http.request.render('PunyaSaudara.penyewaan_report_prompt', {
            "months": MONTHS,
            "years": years
        })

    @http.route('/asset/rentals/report/<year>/<month>', auth='user', website=True)
    def rentals_report(self, year, month, **kw):
        rentals = http.request.env["aset.penyewaan"].search([("month", "=", int(month)),
                                                             ("year", "=", int(year))])
        items = http.request.env["aset.barang"]

        renteds = {}
        returneds = {}
        for rental in rentals:
            for (id, qty) in rental.count_rented_items().items():
                if id not in renteds:
                    renteds[id] = 0
                renteds[id] += qty
            for (id, qty) in rental.count_returned_items().items():
                if id not in returneds:
                    returneds[id] = 0
                returneds[id] += qty

        return http.request.render('PunyaSaudara.penyewaan_report', {
            "items": items,
            "renteds": renteds,
            "returneds": returneds
        })

    @http.route('/asset/returns/report', auth='user', website=True)
    def returns_report_prompt(self, **kw):
        this_year = datetime.now().year
        years = [y for y in range(ESTABLISHMENT_YEAR, this_year + 1)]
        return http.request.render('PunyaSaudara.pengembalian_report_prompt', {
            "months": MONTHS,
            "years": years
        })

    @http.route('/asset/returns/report/<year>/<month>', auth='user', website=True)
    def returns_report(self, year, month, **kw):
        returns = http.request.env["aset.pengembalian"].search([("month", "=", int(month)),
                                                                ("year", "=", int(year))])
        items = http.request.env["aset.barang"]
        returneds = {}

        for return_ in returns:
            for (id, qty) in return_.count_items().items():
                if id not in returneds:
                    returneds[id] = 0
                returneds[id] += qty
        return http.request.render('PunyaSaudara.pengembalian_report', {
            "returneds": returneds,
            "items": items,
        })

    @http.route('/asset/login', auth='public', website=True)
    def login(self, **kw):
        return http.request.render('PunyaSaudara.login', {})
