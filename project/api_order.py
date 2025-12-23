from flask import Blueprint, request, jsonify, session
from sqlalchemy import text
from models import db, ThongBao
from datetime import datetime

order_api_bp = Blueprint('order_api', __name__)

@order_api_bp.route('/api/cap-nhat-mon', methods=['POST'])
def cap_nhat_mon():
    try:
        data = request.json
        update_type = data.get('type')
        status = data.get('status')
        ids_to_process = []

        if update_type == 'single':
            raw_id = data.get('id')
            if raw_id:
                ids_to_process.append(int(raw_id))

        elif update_type == 'group':
            raw_ids = data.get('ids')
            if raw_ids:
                ids_to_process = [int(x) for x in str(raw_ids).split(',')]

        if ids_to_process:
            for single_id in ids_to_process:
                sql_update = text("UPDATE chitietphieugoi SET TrangThai = :tt WHERE ID = :id")
                db.session.execute(sql_update, {'tt': status, 'id': single_id})

                if status == 'HoanTat':
                    create_notification(single_id)

            db.session.commit()
            return jsonify({'success': True, 'msg': 'Cập nhật thành công!'})
        else:
            return jsonify({'success': False, 'msg': 'Không tìm thấy ID món ăn!'})

    except Exception as e:
        db.session.rollback()
        print(f"Lỗi API Bếp: {e}")
        return jsonify({'success': False, 'msg': str(e)})

def create_notification(id_chi_tiet):
    try:
        sql_info = text("""
            SELECT m.TenMon, h.SoBan
            FROM chitietphieugoi cp
            JOIN monan m ON cp.MaMon = m.MaMon
            JOIN phieugoi p ON cp.MaPhieu = p.MaPhieu
            JOIN hoadon h ON p.MaHoaDon = h.MaHoaDon
            WHERE cp.ID = :id
        """)
        res = db.session.execute(sql_info, {'id': id_chi_tiet}).fetchone()

        if res:
            tb = ThongBao(
                NoiDung=f"Bàn {res.SoBan}: {res.TenMon} đã nấu xong!",
                DaXem=False,
                ThoiGian=datetime.now()
            )
            db.session.add(tb)
    except Exception as e:
        print(f"Lỗi tạo thông báo: {e}")

@order_api_bp.route('/api/get-notifications', methods=['GET'])
def get_notifications():
    try:
        sql = text("SELECT * FROM thongbao WHERE DaXem = 0 ORDER BY ThoiGian DESC LIMIT 5")
        result = db.session.execute(sql).fetchall()

        data = [{'msg': r.NoiDung, 'time': r.ThoiGian.strftime('%H:%M')} for r in result]
        return jsonify(data)
    except Exception as e:
        print(f"Lỗi lấy thông báo: {e}")
        return jsonify([])