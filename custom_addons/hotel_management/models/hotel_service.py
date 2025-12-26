# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HotelService(models.Model):
    _name = 'hotel.service'
    _description = 'Dịch vụ đi kèm'
    _order = 'name'

    name = fields.Char(string='Tên dịch vụ', required=True, help='VD: Ăn sáng, Spa, Giặt ủi')
    price = fields.Integer(string='Giá dịch vụ', required=True, default=0, help='Giá của dịch vụ')
    
    _sql_constraints = [
        ('price_positive', 'CHECK(price > 0)', 'Giá dịch vụ phải lớn hơn 0!'),
    ]

