from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

# 1. NHÂN VIÊN
class NhanVien(db.Model):
    __tablename__ = 'NhanVien'
    MaNV = db.Column(db.Integer, primary_key=True)
    TenDangNhap = db.Column(db.String(50), unique=True)
    MatKhau = db.Column(db.String(255))
    HoTen = db.Column(db.String(100))
    VaiTro = db.Column(db.String(20))

# 2. DANH MỤC & MÓN ĂN
class NhomMon(db.Model):
    __tablename__ = 'NhomMon'
    MaNhom = db.Column(db.Integer, primary_key=True)
    TenNhom = db.Column(db.String(50))
    mon_ans = db.relationship('MonAn', backref='nhom', lazy=True)

class MonAn(db.Model):
    __tablename__ = 'MonAn'
    MaMon = db.Column(db.Integer, primary_key=True)
    MaCode = db.Column(db.String(20), unique=True)
    TenMon = db.Column(db.String(100))
    DonVi = db.Column(db.String(50))
    GiaTien = db.Column(db.Numeric(10, 0))
    HinhAnh = db.Column(db.Text)
    DangKinhDoanh = db.Column(db.Boolean, default=True)
    MaNhom = db.Column(db.Integer, db.ForeignKey('NhomMon.MaNhom'))

# 3. BÀN ĂN
class BanAn(db.Model):
    __tablename__ = 'BanAn'
    SoBan = db.Column(db.Integer, primary_key=True)
    TrangThai = db.Column(db.String(20))
    Tang = db.Column(db.Integer, default=1)
    SoGhe = db.Column(db.Integer, default=4)

    # Logic hiển thị cho HTML
    @property
    def css_class(self):
        if self.TrangThai == 'CoKhach': return 'bg-cokhach'
        if self.TrangThai == 'DatTruoc': return 'bg-dattruoc'
        return 'bg-trong'

    @property
    def status_text(self):
        if self.TrangThai == 'CoKhach': return 'Đang phục vụ'
        if self.TrangThai == 'DatTruoc': return 'Đã đặt trước'
        return 'Bàn trống'

    @property
    def icon_class(self):
        if self.TrangThai == 'CoKhach': return 'fa-utensils'
        if self.TrangThai == 'DatTruoc': return 'fa-clock'
        return 'fa-chair'

# 4. HÓA ĐƠN
class HoaDon(db.Model):
    __tablename__ = 'HoaDon'
    MaHoaDon = db.Column(db.Integer, primary_key=True)
    SoBan = db.Column(db.Integer, db.ForeignKey('BanAn.SoBan'))
    MaNV_PhucVu = db.Column(db.Integer, db.ForeignKey('NhanVien.MaNV'))
    ThoiGianVao = db.Column(db.DateTime, default=datetime.now)
    ThoiGianRa = db.Column(db.DateTime, nullable=True)
    TongThanhToan = db.Column(db.Numeric(10, 0), default=0)
    TrangThai = db.Column(db.String(20), default='ChuaThanhToan')
    GhiChu = db.Column(db.String(255))

    chi_tiet = db.relationship('ChiTietHoaDon', backref='hoa_don', lazy=True)

    # Logic kiểm tra hoàn thành đơn
    @property
    def is_completed(self):
        for item in self.chi_tiet:
            if item.TrangThaiMon in ['ChoCheBien', 'DangCheBien']:
                return False
        return True

    @property
    def waited_min(self):
        delta = datetime.now() - self.ThoiGianVao
        return int(delta.total_seconds() / 60)

# 5. CHI TIẾT HÓA ĐƠN
class ChiTietHoaDon(db.Model):
    __tablename__ = 'ChiTietHoaDon'
    MaChiTiet = db.Column(db.Integer, primary_key=True)
    MaHoaDon = db.Column(db.Integer, db.ForeignKey('HoaDon.MaHoaDon'))
    MaMon = db.Column(db.Integer, db.ForeignKey('MonAn.MaMon'))
    SoLuong = db.Column(db.Integer, default=1)
    DonGia = db.Column(db.Numeric(10, 0))
    GhiChu = db.Column(db.String(255))
    TrangThaiMon = db.Column(db.String(20), default='ChoCheBien')
    ThoiGianGoi = db.Column(db.DateTime, default=datetime.now)

    mon_an = db.relationship('MonAn', backref='chi_tiet', lazy=True)

    # Logic CSS màu sắc trạng thái món
    @property
    def status_css(self):
        if self.TrangThaiMon == 'ChoCheBien': return 'st-waiting'
        if self.TrangThaiMon == 'DangCheBien': return 'st-cooking'
        if self.TrangThaiMon == 'HoanTat': return 'st-done'
        if self.TrangThaiMon == 'Served': return 'st-served'
        return ''

# 6. THÔNG BÁO
class ThongBao(db.Model):
    __tablename__ = 'ThongBao'
    MaTB = db.Column(db.Integer, primary_key=True)
    NoiDung = db.Column(db.String(255))
    DaXem = db.Column(db.Boolean, default=False)
    ThoiGian = db.Column(db.DateTime, default=datetime.now)