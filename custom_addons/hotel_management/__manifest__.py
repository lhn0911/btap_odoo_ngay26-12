{
    'name': 'Hotel Management',
    'version': '1.0',
    'category': 'Services',
    'summary': 'Quản lý Khách sạn - Phòng và Đặt phòng',
    'description': """
Quản lý Khách sạn
=================
Module này cho phép quản lý:
- Quản lý Phòng khách sạn (Loại phòng, Giá, Trạng thái)
- Quản lý Đặt phòng (Booking)
- Quản lý Khách hàng
- Quản lý Dịch vụ đi kèm
- Tự động tính toán tổng tiền
    """,
    'depends': ['base'],
    'data': [
        'security/hotel_groups.xml',
        'security/hotel_rules.xml',
        'security/ir.model.access.csv',
        'views/views.xml',
    ],
    'installable': True,
    'application': True,
    'author': 'LHN',
    'license': 'LGPL-3'
}

