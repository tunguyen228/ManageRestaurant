from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify, session
from sqlalchemy import func, text
# Đảm bảo bạn import đúng các model từ file models.py của bạn
from models import db, HoaDon, BanAn, ChiTietHoaDon, ThongBao, NhomMon, MonAn, ChiTietPhieuGoi, PhieuGoi

api_bp = Blueprint('api', __name__)

@api_bp.route('/api/luu-don-hang', methods=['POST'])
def luu_don_hang():
    data = request.json
    so_ban = data.get('so_ban')
    items = data.get('items')
    ma_nv_hien_tai = session.get('id')

    if not so_ban or not items:
        return jsonify({'success': False, 'msg': 'Dữ liệu không hợp lệ'})

    try:
        hoa_don = HoaDon.query.filter_by(SoBan=so_ban, TrangThai='ChuaThanhToan', MaNV_PhucVu=ma_nv_hien_tai).first()

        if not hoa_don:
            hoa_don = HoaDon(SoBan=so_ban, ThoiGianVao=datetime.now(), TrangThai='ChuaThanhToan')
            db.session.add(hoa_don)
            ban = BanAn.query.get(so_ban)
            if ban: ban.TrangThai = 'CoKhach'
            db.session.flush()

        ma_hoa_don = hoa_don.MaHoaDon
        new_phieu = PhieuGoi(MaHoaDon=ma_hoa_don, ThoiGianTao=datetime.now())
        db.session.add(new_phieu)
        db.session.flush()
        ma_phieu = new_phieu.MaPhieu

        for item in items:
            ma_mon = item['id']
            so_luong = int(item['quantity'])
            ghi_chu = item.get('note', '')
            don_gia = float(item['price'])
            ct_phieu = ChiTietPhieuGoi(
                MaPhieu=ma_phieu,
                MaMon=ma_mon,
                SoLuong=so_luong,
                GhiChu=ghi_chu,
                TrangThai='ChoCheBien'
            )
            db.session.add(ct_phieu)
            ct_hoadon = ChiTietHoaDon.query.filter_by(MaHoaDon=ma_hoa_don, MaMon=ma_mon).first()

            if ct_hoadon:
                ct_hoadon.SoLuong += so_luong
            else:
                new_ct = ChiTietHoaDon(
                    MaHoaDon=ma_hoa_don,
                    MaMon=ma_mon,
                    SoLuong=so_luong,
                    DonGia=don_gia
                )
                db.session.add(new_ct)

        db.session.flush()

        sql_update_total = text("""
            UPDATE hoadon 
            SET TongThanhToan = (
                SELECT COALESCE(SUM(SoLuong * DonGia), 0)
                FROM chitiethoadon
                WHERE MaHoaDon = :ma_hd
            )
            WHERE MaHoaDon = :ma_hd
        """)
        db.session.execute(sql_update_total, {'ma_hd': ma_hoa_don})

        db.session.commit()
        return jsonify({'success': True, 'msg': 'Đã gửi bếp thành công!'})

    except Exception as e:
        db.session.rollback()
        print("Lỗi Lưu Đơn:", e)
        return jsonify({'success': False, 'msg': str(e)})

@api_bp.route('/api/checkout', methods=['POST'])
def checkout_bill():
    data = request.json
    ma_hoa_don = data.get('ma_hoa_don')
    tong_thanh_toan = float(data.get('tong_thanh_toan', 0))
    tien_khach_dua = float(data.get('tien_khach_dua', 0))
    giam_gia = float(data.get('giam_gia', 0))

    try:
        hoadon = HoaDon.query.get(ma_hoa_don)
        if not hoadon:
            return jsonify({'success': False, 'msg': 'Không tìm thấy HĐ.'})

        hoadon.TongThanhToan = tong_thanh_toan
        hoadon.GiamGia = giam_gia
        hoadon.TienKhachDua = tien_khach_dua
        tien_thua = tien_khach_dua - tong_thanh_toan
        if tien_thua < 0: tien_thua = 0
        hoadon.TienThua = tien_thua
        hoadon.TrangThai = 'DaThanhToan'
        hoadon.ThoiGianRa = datetime.now()
        ban = BanAn.query.get(hoadon.SoBan)
        if ban: ban.TrangThai = 'Trong'

        db.session.commit()
        return jsonify({'success': True, 'msg': 'Thanh toán thành công!'})

    except Exception as e:
        db.session.rollback()
        print(f"Lỗi Checkout: {e}")
        return jsonify({'success': False, 'msg': f'Lỗi hệ thống: {str(e)}'})

@api_bp.route('/api/get-notifications', methods=['GET'])
def get_notifications():
    notis = ThongBao.query.filter_by(DaXem=False).order_by(ThongBao.ThoiGian.desc()).all()
    data = [{'id': tb.MaTB, 'msg': tb.NoiDung} for tb in notis]
    return jsonify(data)

@api_bp.route('/api/read-notifications', methods=['POST'])
def read_notifications():
    try:
        db.session.query(ThongBao).filter_by(DaXem=False).update({'DaXem': True})
        db.session.commit()
        return jsonify({'success': True})
    except:
        return jsonify({'success': False})

@api_bp.route('/api/get-bill/<int:so_ban>', methods=['GET'])
def get_bill(so_ban):
    try:
        hoadon = HoaDon.query.filter_by(SoBan=so_ban, TrangThai='ChuaThanhToan').first()
        if not hoadon:
            return jsonify({'success': False, 'msg': 'Bàn trống hoặc chưa có hóa đơn.'})

        chi_tiet = ChiTietHoaDon.query.filter_by(MaHoaDon=hoadon.MaHoaDon).all()
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

        vat_rate = 0.1
        vat_amount = tam_tinh * vat_rate
        giam_gia = 0
        tong_tien_sau_vat = tam_tinh + vat_amount
        tong_thanh_toan_cuoi = tong_tien_sau_vat - giam_gia

        return jsonify({
            'success': True,
            'ma_hoa_don': hoadon.MaHoaDon,
            'so_ban': so_ban,
            'thoi_gian_vao': hoadon.ThoiGianVao.strftime('%H:%M %d/%m/%Y'),
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
        print(e)
        return jsonify({'success': False, 'msg': f'Lỗi hệ thống: {str(e)}'})

@api_bp.route('/api/revenue-report', methods=['GET'])
def revenue_report():
    try:
        start_date_str = request.args.get('start_date')
        end_date_str = request.args.get('end_date')

        if not start_date_str or not end_date_str:
            today = datetime.now().date()
            start_date = datetime.combine(today, datetime.min.time())
            end_date = start_date + timedelta(days=1)
        else:
            start_date = datetime.strptime(start_date_str, '%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d') + timedelta(days=1)

        base_query = HoaDon.query.filter(
            HoaDon.TrangThai == 'DaThanhToan',
            HoaDon.ThoiGianVao >= start_date,
            HoaDon.ThoiGianVao < end_date
        )

        total_revenue = base_query.with_entities(func.sum(HoaDon.TongThanhToan)).scalar() or 0
        total_invoices = base_query.count()
        avg_revenue = int(total_revenue / total_invoices) if total_invoices > 0 else 0
        cat_stats = db.session.query(
            NhomMon.TenNhom,
            func.sum(ChiTietHoaDon.SoLuong * ChiTietHoaDon.DonGia)
        ).join(MonAn, MonAn.MaNhom == NhomMon.MaNhom) \
            .join(ChiTietHoaDon, ChiTietHoaDon.MaMon == MonAn.MaMon) \
            .join(HoaDon, HoaDon.MaHoaDon == ChiTietHoaDon.MaHoaDon) \
            .filter(
            HoaDon.TrangThai == 'DaThanhToan',
            HoaDon.ThoiGianVao >= start_date,
            HoaDon.ThoiGianVao < end_date
        ).group_by(NhomMon.TenNhom).all()

        category_data = [{'category': c[0], 'revenue': int(c[1] or 0)} for c in cat_stats]

        top_dishes = db.session.query(
            MonAn.TenMon,
            func.sum(ChiTietHoaDon.SoLuong)
        ).join(ChiTietHoaDon, ChiTietHoaDon.MaMon == MonAn.MaMon) \
            .join(HoaDon, HoaDon.MaHoaDon == ChiTietHoaDon.MaHoaDon) \
            .filter(
            HoaDon.TrangThai == 'DaThanhToan',
            HoaDon.ThoiGianVao >= start_date,
            HoaDon.ThoiGianRa < end_date
        ).group_by(MonAn.TenMon) \
            .order_by(func.sum(ChiTietHoaDon.SoLuong).desc()) \
            .limit(10).all()

        top_dishes_data = [{'dish_name': d[0], 'quantity': int(d[1] or 0)} for d in top_dishes]

        return jsonify({
            'success': True,
            'summary': {
                'total_revenue': int(total_revenue),
                'total_invoices': total_invoices,
                'avg_revenue_per_invoice': avg_revenue,
                'report_period': f"{start_date.strftime('%d/%m/%Y')} - {(end_date - timedelta(days=1)).strftime('%d/%m/%Y')}"
            },
            'category_report': category_data,
            'top_dishes': top_dishes_data
        })

    except Exception as e:
        print("Lỗi Báo Cáo:", e)
        return jsonify({'success': False, 'msg': str(e)})