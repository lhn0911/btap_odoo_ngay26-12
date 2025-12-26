# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HotelCustomer(models.Model):
    _name = 'hotel.customer'
    _description = 'Khách hàng'
    _order = 'name'

    name = fields.Char(string='Tên khách hàng', required=True)
    identity_card = fields.Char(string='Số CMND/CCCD', help='Số chứng minh nhân dân hoặc căn cước công dân')
    phone = fields.Char(string='Số điện thoại')
    
    booking_ids = fields.One2many('hotel.booking', 'customer_id', string='Lịch sử đặt phòng')
    
    _sql_constraints = [
        ('identity_card_unique', 'UNIQUE(identity_card)', 'Số CMND/CCCD đã tồn tại!'),
    ]

