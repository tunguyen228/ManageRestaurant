from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import db, NhanVien, MonAn, BanAn, NhomMon, HoaDon, ChiTietHoaDon
from sqlalchemy import desc, asc, func, text
from datetime import datetime

view_bp = Blueprint('main', __name__)

@view_bp.route('/')
def index():
    if 'loggedin' in session: return redirect_by_role(session['role'])
    return render_template('login.html')

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
        session['avatar'] = user.Avatar
        return redirect_by_role(user.VaiTro)
    flash("Sai tài khoản/mật khẩu", "danger")
    return redirect(url_for('main.index'))

@view_bp.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('main.index'))

def redirect_by_role(role):
    if role == 'PhucVu': return redirect(url_for('main.phucvu'))
    if role == 'Bep': return redirect(url_for('order.bep'))
    if role == 'ThuNgan': return redirect(url_for('main.thungan'))
    if role == 'Admin': return redirect('/admin')
    if role == 'QuanLy': return redirect(url_for('main.quanly'))
    return redirect(url_for('main.index'))

@view_bp.route('/phucvu')
def phucvu():
    if session.get('role') == 'PhucVu':
        ds_ban = BanAn.query.all()
        return render_template('table_list.html', user=session['fullname'], list_ban=ds_ban,
                               avatar_url=session.get('avatar'))
    return redirect(url_for('main.index'))

@view_bp.route('/menu')
def menu():
    if session.get('role') == 'PhucVu':
        selected_table = request.args.get('table_id')
        ds_mon = MonAn.query.filter_by(DangKinhDoanh=True).all()
        ds_nhom = NhomMon.query.all()
        ds_ban = BanAn.query.all()
        return render_template('menu.html', user=session['fullname'], menu=ds_mon, categories=ds_nhom, tables=ds_ban,
                               selected_table=selected_table, avatar_url=session.get('avatar'))
    return redirect(url_for('main.index'))

@view_bp.route('/thungan')
def thungan():
    list_ban = BanAn.query.filter_by(TrangThai='CoKhach').all()

    return render_template('cashier.html',
                           list_ban=list_ban,
                           user="Thu Ngân Viên",
                           avatar_url="")

@view_bp.route('/quanly')
def quanly():
    if session.get('role') in ['QuanLy', 'Admin']:
        return render_template('manager.html', user=session['fullname'], avatar_url=session.get('avatar'))
    return redirect(url_for('main.index'))