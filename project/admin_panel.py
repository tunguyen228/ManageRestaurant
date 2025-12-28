from flask import redirect, url_for, session, flash
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
#from flask_babel import Babel
from models import db, MonAn, NhomMon, NhanVien

class SecureModelView(ModelView):
    def is_accessible(self):
        return 'loggedin' in session and session.get('role') == 'Admin'

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('main.index'))

class DishModelView(SecureModelView):
    create_template = 'admin/custom_form.html'
    edit_template = 'admin/custom_form.html'

    column_list = ('MaCode', 'TenMon', 'GiaTien', 'nhom', 'DangKinhDoanh')
    column_searchable_list = ['MaCode', 'TenMon']
    column_filters = ['nhom', 'GiaTien', 'DangKinhDoanh']
    form_columns = ('MaCode', 'TenMon', 'nhom', 'GiaTien', 'HinhAnh', 'DangKinhDoanh')

    column_labels = {
        'MaCode': ('Mã món'),
        'TenMon': ('Tên món'),
        'GiaTien': ('Giá'),
        'nhom': ('Nhóm món'),
        'DangKinhDoanh': ('Đang kinh doanh'),
        'HinhAnh': ('Hình ảnh')
    }

class CategoryModelView(SecureModelView):
    create_template = 'admin/custom_form.html'
    edit_template = 'admin/custom_form.html'

    column_list = ('MaNhom', 'TenNhom')
    form_columns = ('TenNhom',)
    column_labels = {'MaNhom': ('Mã nhóm'), 'TenNhom': ('Tên nhóm')}

class StaffModelView(SecureModelView):
    create_template = 'admin/custom_form.html'
    edit_template = 'admin/custom_form.html'

    column_list = ('TenDangNhap', 'MatKhau','HoTen', 'VaiTro')

    column_labels = {
        'TenDangNhap': 'Tên đăng nhập',
        'MatKhau': 'Mật khẩu',
        'HoTen': 'Họ tên',
        'VaiTro': 'Vai trò',
        'NgayTao': 'Ngày tạo',
        'Avatar': 'Ảnh đại diện'
    }

    form_columns = ('TenDangNhap', 'MatKhau', 'HoTen', 'VaiTro', 'Avatar')

class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return 'loggedin' in session and session.get('role') == 'Admin'

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('main.index'))

    @expose('/')
    def index(self):
        return self.render('admin/index.html',
                           user=session.get('fullname'),
                           avatar_url=session.get('avatar'))

def init_admin(app, db):
    admin = Admin(app, name=('PTT Quản Trị'), index_view=MyAdminIndexView())
    admin.add_view(DishModelView(MonAn, db.session, name=("Thực Đơn")))
    admin.add_view(CategoryModelView(NhomMon, db.session, name=("Nhóm Món")))
    admin.add_view(StaffModelView(NhanVien, db.session, name=("Nhân Viên")))