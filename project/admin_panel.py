from flask import redirect, url_for, session, flash
from flask_admin import Admin, AdminIndexView, expose
from flask_admin.contrib.sqla import ModelView
from models import db, MonAn, NhomMon
from wtforms.validators import DataRequired, NumberRange


# 1. Bảo vệ quyền Admin
class SecureModelView(ModelView):
    def is_accessible(self):
        return 'loggedin' in session and session.get('role') == 'Admin'

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('main.index'))


# 2. Ẩn khỏi menu mặc định (Để dùng Dashboard thẻ bài)
class HiddenModelView(SecureModelView):
    def is_visible(self):
        return False


# 3. View Quản lý Món ăn
class DishModelView(HiddenModelView):
    # Sử dụng template form tùy chỉnh để giao diện đẹp hơn
    create_template = 'admin/custom_form.html'
    edit_template = 'admin/custom_form.html'

    column_list = ('MaCode', 'TenMon', 'GiaTien', 'nhom', 'DangKinhDoanh')
    column_searchable_list = ['MaCode', 'TenMon']
    column_filters = ['nhom', 'GiaTien', 'DangKinhDoanh']
    form_columns = ('MaCode', 'TenMon', 'nhom', 'GiaTien', 'HinhAnh', 'DangKinhDoanh')

    column_labels = {
        'MaCode': 'Mã', 'TenMon': 'Tên Món', 'GiaTien': 'Giá',
        'nhom': 'Nhóm', 'DangKinhDoanh': 'Bán', 'HinhAnh': 'Ảnh'
    }

    form_args = {
        'GiaTien': {'validators': [DataRequired(), NumberRange(min=1)]},
        'MaCode': {'validators': [DataRequired()]}
    }


# 4. View Quản lý Nhóm
class CategoryModelView(HiddenModelView):
    column_list = ('MaNhom', 'TenNhom')
    form_columns = ('TenNhom',)
    column_labels = {'MaNhom': 'ID', 'TenNhom': 'Tên Nhóm'}


# 5. Dashboard Index
class MyAdminIndexView(AdminIndexView):
    def is_accessible(self):
        return 'loggedin' in session and session.get('role') == 'Admin'

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('main.index'))

    @expose('/')
    def index(self):
        return self.render('admin.html',
                           user=session.get('fullname'),
                           avatar_url=session.get('avatar'))


# 6. Hàm khởi tạo
def init_admin(app, db):
    admin = Admin(app, name='PTT Admin',
                  index_view=MyAdminIndexView(template='admin.html'))

    # Gán template master tại đây
    admin.base_template = 'admin/master.html'

    admin.add_view(DishModelView(MonAn, db.session, name="Thực Đơn", endpoint='monan'))
    admin.add_view(CategoryModelView(NhomMon, db.session, name="Nhóm Món", endpoint='nhommon'))