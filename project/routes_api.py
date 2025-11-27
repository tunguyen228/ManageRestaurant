from flask import Blueprint, request, jsonify, session
from models import db, HoaDon, BanAn, ChiTietHoaDon, ThongBao
from datetime import datetime

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
@api_bp.route('/api/thanh-toan', methods=['POST'])
def thanh_toan():
    if not session.get('loggedin'): return jsonify({'success': False, 'msg': 'Chưa đăng nhập'})
    data = request.json
    ma_hoa_don = data.get('ma_hoa_don')

    try:
        hoa_don = HoaDon.query.get(ma_hoa_don)
        if hoa_don:
            hoa_don.TrangThai = 'DaThanhToan'
            hoa_don.ThoiGianRa = datetime.now()
            ban = BanAn.query.get(hoa_don.SoBan)
            ban.TrangThai = 'Trong'
            db.session.commit()
            return jsonify({'success': True, 'msg': 'Thanh toán thành công!'})
        return jsonify({'success': False, 'msg': 'Không tìm thấy HĐ'})
    except Exception as e:
        db.session.rollback()
        return jsonify({'success': False, 'msg': str(e)})


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