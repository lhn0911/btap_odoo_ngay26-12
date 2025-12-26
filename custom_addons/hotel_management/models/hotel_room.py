# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HotelRoom(models.Model):
    _name = 'hotel.room'
    _description = 'Phòng Khách sạn'
    _order = 'name'

    name = fields.Char(string='Số phòng', required=True, help='VD: P101, P205')
    floor = fields.Integer(string='Tầng', help='Tầng của phòng')
    price_per_night = fields.Integer(string='Giá thuê 1 đêm', required=True, default=0)
    status = fields.Selection(
        string='Trạng thái',
        selection=[
            ('available', 'Trống'),
            ('occupied', 'Đang ở'),
            ('maintenance', 'Bảo trì')
        ],
        default='available',
        required=True
    )
    
    # Quan hệ
    type_id = fields.Many2one('hotel.room.type', string='Loại phòng', required=True)
    
    # Quan hệ ngược
    booking_ids = fields.One2many('hotel.booking', 'room_id', string='Lịch sử đặt phòng')
    
    _sql_constraints = [
        ('name_unique', 'UNIQUE(name)', 'Số phòng đã tồn tại!'),
        ('price_positive', 'CHECK(price_per_night > 0)', 'Giá phòng phải lớn hơn 0!'),
    ]

