# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError
from datetime import datetime, timedelta
from dateutil.relativedelta import relativedelta


class HotelBooking(models.Model):
    _name = 'hotel.booking'
    _description = 'Phiếu Đặt phòng'
    _order = 'check_in desc, code'

    code = fields.Char(string='Mã booking', help='Mã đặt phòng (tự nhập)')
    check_in = fields.Date(string='Ngày nhận phòng', required=True, default=fields.Date.today)
    check_out = fields.Date(string='Ngày trả phòng', required=True)
    duration = fields.Integer(string='Số đêm lưu trú', compute='_compute_duration', store=True, readonly=True)
    total_amount = fields.Integer(string='Tổng thành tiền', compute='_compute_total_amount', store=True, readonly=True)
    state = fields.Selection(
        string='Trạng thái',
        selection=[
            ('draft', 'Nháp'),
            ('confirmed', 'Đã xác nhận'),
            ('done', 'Hoàn thành')
        ],
        default='draft',
        required=True
    )
    
    # Quan hệ
    customer_id = fields.Many2one('hotel.customer', string='Khách hàng', required=True)
    room_id = fields.Many2one('hotel.room', string='Phòng', required=True)
    service_ids = fields.Many2many('hotel.service', string='Dịch vụ thêm')
    
    @api.depends('check_in', 'check_out')
    def _compute_duration(self):
        """Tính số đêm lưu trú"""
        for record in self:
            if record.check_in and record.check_out:
                delta = record.check_out - record.check_in
                record.duration = delta.days if delta.days > 0 else 0
            else:
                record.duration = 0
    
    @api.depends('room_id', 'duration', 'service_ids')
    def _compute_total_amount(self):
        """Tính tổng thành tiền: (Giá phòng * Số đêm) + Tổng tiền dịch vụ"""
        for record in self:
            total = 0
            # Tiền phòng
            if record.room_id and record.duration:
                total += record.room_id.price_per_night * record.duration
            # Tiền dịch vụ
            if record.service_ids:
                total += sum(record.service_ids.mapped('price'))
            record.total_amount = total
    
    @api.onchange('check_in')
    def _onchange_check_in(self):
        """Tự động điền ngày trả phòng = ngày nhận + 1 ngày"""
        if self.check_in:
            check_in_date = fields.Date.from_string(self.check_in) if isinstance(self.check_in, str) else self.check_in
            self.check_out = check_in_date + relativedelta(days=1)
    
    @api.onchange('room_id')
    def _onchange_room_id(self):
        """Cảnh báo nếu phòng đang bảo trì"""
        if self.room_id and self.room_id.status == 'maintenance':
            return {
                'warning': {
                    'title': 'Cảnh báo',
                    'message': 'Phòng này đang bảo trì, vui lòng chọn phòng khác!'
                }
            }
    
    @api.constrains('check_in', 'check_out')
    def _check_dates(self):
        """Kiểm tra ngày trả phải lớn hơn ngày nhận"""
        for record in self:
            if record.check_in and record.check_out:
                if record.check_out <= record.check_in:
                    raise ValidationError('Ngày trả phòng không hợp lệ!')
    
    @api.constrains('room_id')
    def _check_room_status(self):
        """Chặn đặt phòng đang có người ở"""
        for record in self:
            if record.room_id and record.room_id.status == 'occupied':
                raise ValidationError('Phòng này đang có khách ở!')

