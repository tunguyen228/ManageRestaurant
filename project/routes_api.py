from flask import Blueprint, request, jsonify, session
from models import db, HoaDon, BanAn, ChiTietHoaDon, ThongBao, NhomMon, MonAn
from sqlalchemy import func
from datetime import datetime, timedelta

api_bp = Blueprint('api', __name__)


# 1. API LƯU ĐƠN HÀNG
@api_bp.route('/api/luu-don-hang', methods=['POST'])
def luu_don_hang():
    if not session.get('loggedin'): return jsonify({'success': False, 'msg': 'Chưa đăng nhập'})
    data = request.json
    so_ban = data.get('so_ban')
    items = data.get('items')

    if not so_ban or not items: return jsonify({'success': False, 'msg': 'Dữ liệu lỗi'})

    try:
        hoa_don = HoaDon.query.filter_by(SoBan=so_ban, TrangThai='ChuaThanhToan').first()
        if not hoa_don:
            hoa_don = HoaDon(SoBan=so_ban, MaNV_PhucVu=session['id'], ThoiGianVao=datetime.now())
            db.session.add(hoa_don)
            ban = BanAn.query.get(so_ban)
            ban.TrangThai = 'CoKhach'
            db.session.commit()

        tong_them = 0
        for item in items:
            ct = ChiTietHoaDon(
                MaHoaDon=hoa_don.MaHoaDon,
                MaMon=item['id'],
                SoLuong=item['quantity'],
                DonGia=item['price'],
                GhiChu=item.get('note', ''),
                TrangThaiMon='ChoCheBien'
            )
            db.session.add(ct)
            tong_them += (item['quantity'] * item['price'])

        hoa_don.TongThanhToan += tong_them
        db.session.commit()
        return jsonify({'success': True, 'msg': 'Gửi đơn thành công!'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'msg': str(e)})


# 2. API THANH TOÁN
# @api_bp.route('/api/thanh-toan', methods=['POST'])
# def thanh_toan():
#     if not session.get('loggedin'): return jsonify({'success': False, 'msg': 'Chưa đăng nhập'})
#     data = request.json
#     ma_hoa_don = data.get('ma_hoa_don')
#
#     try:
#         hoa_don = HoaDon.query.get(ma_hoa_don)
#         if hoa_don:
#             hoa_don.TrangThai = 'DaThanhToan'
#             hoa_don.ThoiGianRa = datetime.now()
#             ban = BanAn.query.get(hoa_don.SoBan)
#             ban.TrangThai = 'Trong'
#             db.session.commit()
#             return jsonify({'success': True, 'msg': 'Thanh toán thành công!'})
#         return jsonify({'success': False, 'msg': 'Không tìm thấy HĐ'})
#     except Exception as e:
#         db.session.rollback()
#         return jsonify({'success': False, 'msg': str(e)})
@api_bp.route('/api/checkout', methods=['POST'])
def checkout_bill():
    if not session.get('loggedin'):
        return jsonify({'success': False, 'msg': 'Chưa đăng nhập'}), 401

    data = request.json
    ma_hoa_don = data.get('ma_hoa_don')
    tong_thanh_toan = data.get('tong_thanh_toan')
    giam_gia = data.get('giam_gia')

    if not ma_hoa_don:
        return jsonify({'success': False, 'msg': 'Thiếu mã hóa đơn.'})

    try:
        hoa_don = HoaDon.query.get(ma_hoa_don)
        if not hoa_don:
            return jsonify({'success': False, 'msg': 'Không tìm thấy HĐ.'})

        hoa_don.TongThanhToan = tong_thanh_toan
        hoa_don.GiamGia = giam_gia

        hoa_don.TrangThai = 'DaThanhToan'
        hoa_don.ThoiGianRa = datetime.now()

        ban = BanAn.query.get(hoa_don.SoBan)
        ban.TrangThai = 'Trong'

        db.session.commit()
        return jsonify({'success': True, 'msg': 'Thanh toán thành công!'})

    except Exception as e:
        db.session.rollback()
        # Thêm log lỗi nếu cần thiết
        return jsonify({'success': False, 'msg': f'Lỗi hệ thống: {str(e)}'})


# 3. API CẬP NHẬT TRẠNG THÁI MÓN (CHO BẾP & PHỤC VỤ)
@api_bp.route('/api/update-status', methods=['POST'])
def update_status():
    data = request.json
    raw_id = data.get('id')
    status = data.get('status')

    try:
        id_list = []
        if isinstance(raw_id, str) and ',' in raw_id:
            id_list = [int(x) for x in raw_id.split(',')]
        else:
            id_list = [int(raw_id)]

        mon_ans = db.session.query(ChiTietHoaDon).filter(ChiTietHoaDon.MaChiTiet.in_(id_list)).all()

        for mon in mon_ans:
            mon.TrangThaiMon = status
            # Nếu Bếp xong -> Tạo thông báo
            if status == 'HoanTat':
                hd = HoaDon.query.get(mon.MaHoaDon)
                tb = ThongBao(
                    NoiDung=f"Bàn {hd.SoBan}: {mon.mon_an.TenMon} đã nấu xong!",
                    DaXem=False
                )
                db.session.add(tb)

        db.session.commit()
        return jsonify({'success': True})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'msg': str(e)})


# 4. API LẤY THÔNG BÁO
@api_bp.route('/api/get-notifications', methods=['GET'])
def get_notifications():
    notis = ThongBao.query.filter_by(DaXem=False).order_by(ThongBao.ThoiGian.desc()).all()
    data = [{'id': tb.MaTB, 'msg': tb.NoiDung} for tb in notis]
    return jsonify(data)


# 5. API ĐỌC THÔNG BÁO
@api_bp.route('/api/read-notifications', methods=['POST'])
def read_notifications():
    try:
        db.session.query(ThongBao).filter_by(DaXem=False).update({'DaXem': True})
        db.session.commit()
        return jsonify({'success': True})
    except:
        return jsonify({'success': False})


# --- 6. API LẤY CHI TIẾT HÓA ĐƠN VÀ TÍNH TOÁN ---
@api_bp.route('/api/get-bill/<int:so_ban>', methods=['GET'])
def get_bill(so_ban):
    try:
        hoa_don = HoaDon.query.filter_by(SoBan=so_ban, TrangThai='ChuaThanhToan').first()
        if not hoa_don:
            return jsonify({'success': False, 'msg': 'Bàn trống hoặc chưa có hóa đơn.'})

        chi_tiet = hoa_don.chi_tiet

        items_list = []
        tam_tinh = 0

        for item in chi_tiet:
            thanh_tien = int(item.SoLuong) * int(item.DonGia)
            tam_tinh += thanh_tien
            items_list.append({
                'ten_mon': item.mon_an.TenMon,
                'so_luong': item.SoLuong,
                'don_gia': int(item.DonGia),
                'thanh_tien': thanh_tien,
                'ghi_chu': item.GhiChu
            })

        vat_rate = 0.10
        vat_amount = tam_tinh * vat_rate

        tong_tien_sau_vat = tam_tinh + vat_amount

        giam_gia = 0
        if tong_tien_sau_vat > 500000:
            giam_gia_rate = 0.05
            giam_gia = tong_tien_sau_vat * giam_gia_rate

        tong_thanh_toan_cuoi = tong_tien_sau_vat - giam_gia

        return jsonify({
            'success': True,
            'ma_hoa_don': hoa_don.MaHoaDon,
            'so_ban': so_ban,
            'thoi_gian_vao': hoa_don.ThoiGianVao.strftime('%H:%M %d/%m/%Y'),
            'items': items_list,
            'calculations': {
                'tong_so_luong': sum(i['so_luong'] for i in items_list),
                'tam_tinh': round(tam_tinh),
                'vat': round(vat_amount),
                'giam_gia': round(giam_gia),
                'tong_thanh_toan': round(tong_thanh_toan_cuoi)
            }
        })

    except Exception as e:
        return jsonify({'success': False, 'msg': f'Lỗi hệ thống: {str(e)}'})


# --- 7. API BÁO CÁO DOANH THU ---
@api_bp.route('/api/revenue-report', methods=['GET'])
def revenue_report():
    if session.get('role') not in ['QuanLy', 'Admin']:
        return jsonify({'success': False, 'msg': 'Không có quyền truy cập'}), 403

    today = datetime.now().date()

    start_date_str = request.args.get('start_date', today.strftime('%Y-%m-%d'))
    end_date_str = request.args.get('end_date', today.strftime('%Y-%m-%d'))

    try:
        start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
        end_date = datetime.strptime(end_date_str, '%Y-%m-%d') + timedelta(days=1)
    except ValueError:
        return jsonify({'success': False, 'msg': 'Định dạng ngày không hợp lệ. Yêu cầu YYYY-MM-DD.'}), 400

    base_query = db.session.query(HoaDon).filter(
        HoaDon.TrangThai == 'DaThanhToan',
        HoaDon.ThoiGianRa >= start_date,
        HoaDon.ThoiGianRa < end_date
    )

    total_revenue = db.session.query(func.sum(HoaDon.TongThanhToan)).filter(
        HoaDon.TrangThai == 'DaThanhToan',
        HoaDon.ThoiGianRa >= start_date,
        HoaDon.ThoiGianRa < end_date
    ).scalar() or 0

    total_invoices = base_query.count()

    avg_revenue_per_invoice = round(total_revenue / total_invoices) if total_invoices else 0

    revenue_by_category = db.session.query(
        NhomMon.TenNhom,
        func.sum(ChiTietHoaDon.SoLuong * ChiTietHoaDon.DonGia).label('DoanhThuNhom')
    ).join(MonAn, NhomMon.MaNhom == MonAn.MaNhom) \
        .join(ChiTietHoaDon, MonAn.MaMon == ChiTietHoaDon.MaMon) \
        .join(HoaDon, ChiTietHoaDon.MaHoaDon == HoaDon.MaHoaDon) \
        .filter(
        HoaDon.TrangThai == 'DaThanhToan',
        HoaDon.ThoiGianRa >= start_date,
        HoaDon.ThoiGianRa < end_date
    ).group_by(NhomMon.TenNhom).order_by(func.sum(ChiTietHoaDon.SoLuong).desc()).all()

    category_data = [{
        'category': r.TenNhom,
        'revenue': int(r.DoanhThuNhom)
    } for r in revenue_by_category]

    top_selling_dishes = db.session.query(
        MonAn.TenMon,
        func.sum(ChiTietHoaDon.SoLuong).label('TotalSold')
    ).join(ChiTietHoaDon, MonAn.MaMon == ChiTietHoaDon.MaMon) \
        .join(HoaDon, ChiTietHoaDon.MaHoaDon == HoaDon.MaHoaDon) \
        .filter(
        HoaDon.TrangThai == 'DaThanhToan',
        HoaDon.ThoiGianRa >= start_date,
        HoaDon.ThoiGianRa < end_date
    ).group_by(MonAn.TenMon).order_by(func.sum(ChiTietHoaDon.SoLuong).desc()).limit(10).all()

    top_dishes_data = [{
        'dish_name': d.TenMon,
        'quantity': int(d.TotalSold)
    } for d in top_selling_dishes]

    if total_invoices == 0:
        return jsonify({'success': False, 'msg': 'Không có hóa đơn nào trong khoảng thời gian đã chọn.'})

    return jsonify({
        'success': True,
        'summary': {
            'total_revenue': int(total_revenue),
            'total_invoices': total_invoices,
            'avg_revenue_per_invoice': avg_revenue_per_invoice,
            'report_period': f"{start_date_str} đến {end_date_str}"
        },
        'category_report': category_data,
        'top_dishes': top_dishes_data
    })