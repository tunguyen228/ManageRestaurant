from flask import redirect, url_for, session, flash
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_admin.menu import MenuLink
# 👇 Bỏ NhanVien, BanAn, HoaDon khỏi dòng import nếu không dùng
from .models import db, MonAn, NhomMon
from wtforms.validators import DataRequired, NumberRange


# 1. Lớp Bảo vệ: Chỉ cho phép vai trò 'Admin' truy cập
class SecureModelView(ModelView):
    def is_accessible(self):
        return 'loggedin' in session and session.get('role') == 'Admin'

    def inaccessible_callback(self, name, **kwargs):
        flash('Bạn không có quyền truy cập trang Quản trị!', 'danger')
        return redirect(url_for('main.index'))


# 2. Tùy chỉnh giao diện Quản lý Món ăn
class DishModelView(SecureModelView):
    # Danh sách cột hiển thị (Đã bỏ DonVi)
    column_list = ('MaCode', 'TenMon', 'GiaTien', 'nhom', 'DangKinhDoanh')

    column_searchable_list = ['MaCode', 'TenMon']

    column_filters = ['nhom', 'GiaTien', 'DangKinhDoanh']

    # Form nhập liệu (Đã bỏ DonVi)
    form_columns = ('MaCode', 'TenMon', 'nhom', 'GiaTien', 'HinhAnh', 'DangKinhDoanh')

    # Tên hiển thị tiếng Việt (Đã xóa dòng 'DonVi': 'Đơn Vị')
    column_labels = {
        'MaCode': 'Mã Món',
        'TenMon': 'Tên Món',
        'GiaTien': 'Giá Bán',
        'nhom': 'Nhóm Món',
        'DangKinhDoanh': 'Đang Bán',
        'HinhAnh': 'Link Ảnh'
    }

    form_args = {
        'GiaTien': {'validators': [DataRequired(), NumberRange(min=1)]},
        'MaCode': {'validators': [DataRequired()]}
    }


# 3. Class cho trang chủ Admin
class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return 'loggedin' in session and session.get('role') == 'Admin'

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('main.index'))


# 4. Hàm khởi tạo
def init_admin(app, db):
    admin = Admin(app, name='PTT Quản Trị', index_view=MyAdminIndexView())

    # CHỈ CÒN LẠI THỰC ĐƠN VÀ NHÓM MÓN
    admin.add_view(DishModelView(MonAn, db.session, name="Thực Đơn"))
    admin.add_view(SecureModelView(NhomMon, db.session, name="Nhóm Món"))

    # Nút đăng xuất
    admin.add_link(MenuLink(name='Đăng xuất', category='', url='/logout'))