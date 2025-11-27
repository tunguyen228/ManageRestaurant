from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import db, NhanVien, MonAn, BanAn, NhomMon, HoaDon, ChiTietHoaDon
from sqlalchemy import desc, asc, func
from datetime import datetime

view_bp = Blueprint('main', __name__)

# --- AUTHENTICATION ---
@view_bp.route('/')
def index():
    if 'loggedin' in session: return redirect_by_role(session['role'])
    return render_template('index.html')

@view_bp.route('/login', methods=['POST'])
def login():
    username = request.form.get('username')
    password = request.form.get('password')
    user = NhanVien.query.filter_by(TenDangNhap=username, MatKhau=password).first()
    if user:
        session['loggedin'] = True
        session['id'] = user.MaNV
        session['username'] = user.TenDangNhap
        session['fullname'] = user.HoTen
        session['role'] = user.VaiTro
        return redirect_by_role(user.VaiTro)
    flash("Sai tài khoản/mật khẩu", "danger")
    return redirect(url_for('main.index'))

@view_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.index'))

def redirect_by_role(role):
    if role == 'PhucVu': return redirect(url_for('main.phucvu'))
    if role == 'Bep': return redirect(url_for('main.bep'))
    if role == 'ThuNgan': return redirect(url_for('main.thungan'))
    if role == 'Admin': return redirect('/admin')
    if role == 'QuanLy': return redirect(url_for('main.quanly'))
    return redirect(url_for('main.index'))

# --- 1. TABLE LIST (SƠ ĐỒ BÀN) ---
@view_bp.route('/phucvu')
def phucvu():
    if session.get('role') == 'PhucVu':
        ds_ban = BanAn.query.all()
        # Không cần xử lý logic CSS ở đây nữa, Model đã lo
        return render_template('phucvu.html', user=session['fullname'], list_ban=ds_ban)
    return redirect(url_for('main.index'))

# --- 2. MENU (GỌI MÓN) ---
@view_bp.route('/menu')
def menu():
    if session.get('role') == 'PhucVu':
        selected_table = request.args.get('table_id')
        ds_mon = MonAn.query.filter_by(DangKinhDoanh=True).all()
        ds_nhom = NhomMon.query.all()
        ds_ban = BanAn.query.all()
        return render_template('menu.html', user=session['fullname'], menu=ds_mon, categories=ds_nhom, tables=ds_ban, selected_table=selected_table)
    return redirect(url_for('main.index'))

# --- 3. ORDER LIST (DANH SÁCH ĐƠN - ĐÃ TỐI ƯU) ---
@view_bp.route('/order-list')
def order_list():
    if session.get('role') == 'PhucVu':
        # Chỉ cần query, logic tính phút chờ và hoàn thành đã nằm trong Model HoaDon
        ds_hoa_don = HoaDon.query.filter_by(TrangThai='ChuaThanhToan').order_by(desc(HoaDon.ThoiGianVao)).all()
        return render_template('order_list.html', user=session['fullname'], orders=ds_hoa_don, now=datetime.now())
    return redirect(url_for('main.index'))

# --- 4. BẾP (LOGIC NẤU GỘP & TÁCH) ---
@view_bp.route('/bep')
def bep():
    if session.get('role') == 'Bep':
        mode = request.args.get('mode', 'order')

        # Danh sách Đang nấu
        cooking_list = ChiTietHoaDon.query.filter_by(TrangThaiMon='DangCheBien').order_by(ChiTietHoaDon.ThoiGianGoi.asc()).all()
        waiting_list = []

        if mode == 'order':
            # Chế độ chi tiết
            waiting_list = db.session.query(ChiTietHoaDon)\
                .join(HoaDon)\
                .filter(ChiTietHoaDon.TrangThaiMon == 'ChoCheBien')\
                .order_by(ChiTietHoaDon.ThoiGianGoi.asc())\
                .all()
        else:
            # Chế độ gộp món (Dish) - Sửa lại logic SUM
            results = db.session.query(
                MonAn.TenMon,
                func.sum(ChiTietHoaDon.SoLuong).label('SoLuongGop'), # Dùng SUM
                func.group_concat(ChiTietHoaDon.MaChiTiet).label('ListIDs')
            )\
            .join(MonAn, ChiTietHoaDon.MaMon == MonAn.MaMon)\
            .filter(ChiTietHoaDon.TrangThaiMon == 'ChoCheBien')\
            .group_by(MonAn.TenMon)\
            .order_by(func.min(ChiTietHoaDon.ThoiGianGoi).asc())\
            .all()

            for row in results:
                waiting_list.append({
                    'TenMon': row.TenMon,
                    'SoLuong': int(row.SoLuongGop) if row.SoLuongGop else 0,
                    'IDs': row.ListIDs,
                    'IsAggregated': True
                })

        return render_template('bep.html', user=session['fullname'], waiting_list=waiting_list, cooking_list=cooking_list, mode=mode)
    return redirect(url_for('main.index'))

# --- VIEWS KHÁC ---
@view_bp.route('/thungan')
def thungan(): return render_template('thungan.html', user=session['fullname'])
@view_bp.route('/quanly')
def quanly(): return render_template('quanly.html', user=session['fullname'])