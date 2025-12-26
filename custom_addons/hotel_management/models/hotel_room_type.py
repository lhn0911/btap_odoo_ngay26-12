# -*- coding: utf-8 -*-

from odoo import models, fields, api


class HotelRoomType(models.Model):
    _name = 'hotel.room.type'
    _description = 'Loại Phòng Khách sạn'
    _order = 'name'

    name = fields.Char(string='Tên loại phòng', required=True, help='VD: Single, Double, VIP')
    code = fields.Char(string='Mã loại', help='Mã định danh loại phòng')
    
    # Quan hệ ngược
    room_ids = fields.One2many('hotel.room', 'type_id', string='Danh sách phòng')

