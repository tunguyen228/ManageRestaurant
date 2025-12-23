from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from models import db, NhanVien, MonAn, BanAn, NhomMon, HoaDon, ChiTietHoaDon
from sqlalchemy import desc, asc, func, text
from datetime import datetime
view_bp = Blueprint('order', __name__)

@view_bp.route('/order-list')
def order_list():
    if session.get('role') != 'PhucVu':
        return redirect(url_for('main.index'))

    sql_orders = text("""
                      SELECT h.MaHoaDon, h.SoBan, h.ThoiGianVao, h.TongThanhToan AS TongThanhToan
                      FROM hoadon h
                      WHERE h.TrangThai = 'ChuaThanhToan'
                      ORDER BY h.ThoiGianVao DESC
                      """)
    orders_data = []
    try:
        orders_result = db.session.execute(sql_orders).fetchall()

        for ord in orders_result:
            sql_details = text("""
                        SELECT cp.ID AS MaChiTiet, m.TenMon, cp.SoLuong, cp.TrangThai AS TrangThaiMon, cp.GhiChu
                        FROM chitietphieugoi cp
                        JOIN monan m ON cp.MaMon = m.MaMon
                        JOIN phieugoi p ON cp.MaPhieu = p.MaPhieu
                        WHERE p.MaHoaDon = :ma_hd
                        ORDER BY cp.ID DESC
            """)
            details = db.session.execute(sql_details, {'ma_hd': ord.MaHoaDon}).fetchall()
            is_completed = all(d.TrangThaiMon == 'DaPhucVu' for d in details) if details else False
            waited_min = 0
            if ord.ThoiGianVao:
                delta = datetime.now() - ord.ThoiGianVao
                waited_min = int(delta.total_seconds() / 60)

            orders_data.append({
                'MaHoaDon': ord.MaHoaDon,
                'SoBan': ord.SoBan,
                'ThoiGianVao': ord.ThoiGianVao,
                'TongThanhToan': ord.TongThanhToan if ord.TongThanhToan else 0,
                'chi_tiet': details,
                'is_completed': is_completed,
                'waited_min': waited_min
            })
    except Exception as e:
        print("Lỗi Order List:", e)

    return render_template('order_list.html',
                           orders=orders_data,
                           now=datetime.now(),
                           user=session.get('fullname'),
                           avatar_url=session.get('avatar'))
@view_bp.route('/bep')
def bep():
    if session.get('role') != 'Bep': return redirect(url_for('main.index'))
    mode = request.args.get('mode', 'order')
    waiting_list = []
    cooking_list = []
    try:
        if mode == 'dish':
            sql_waiting = text("""
                    SELECT m.TenMon, SUM(cp.SoLuong) AS TongSoLuong,
                            GROUP_CONCAT(h.SoBan ORDER BY h.SoBan ASC SEPARATOR ', ') AS CacBan,
                            GROUP_CONCAT(cp.ID SEPARATOR ',') AS ListIDs,
                            MIN(p.ThoiGianTao) AS ThoiGianSomNhat
                    FROM chitietphieugoi cp
                    JOIN phieugoi p ON cp.MaPhieu = p.MaPhieu
                    JOIN hoadon h ON p.MaHoaDon = h.MaHoaDon
                    JOIN monan m ON cp.MaMon = m.MaMon
                    WHERE cp.TrangThai = 'ChoCheBien'
                    GROUP BY m.TenMon
                    ORDER BY ThoiGianSomNhat ASC
            """)
            result_waiting = db.session.execute(sql_waiting).fetchall()
            for row in result_waiting:
                waiting_list.append(
                    {'IsAggregated': True, 'TenMon': row.TenMon, 'SoLuong': int(row.TongSoLuong), 'SoBan': row.CacBan,
                     'IDs': row.ListIDs, 'ThoiGian': row.ThoiGianSomNhat.strftime('%H:%M')})
        else:
            sql_waiting = text("""
                SELECT cp.ID, m.TenMon, cp.SoLuong, h.SoBan, cp.GhiChu, p.ThoiGianTao
                FROM chitietphieugoi cp
                JOIN phieugoi p ON cp.MaPhieu = p.MaPhieu
                JOIN hoadon h ON p.MaHoaDon = h.MaHoaDon
                JOIN monan m ON cp.MaMon = m.MaMon
                WHERE cp.TrangThai = 'ChoCheBien'
                ORDER BY p.ThoiGianTao ASC
            """)
            result_waiting = db.session.execute(sql_waiting).fetchall()
            for row in result_waiting:
                waiting_list.append(
                    {'IsAggregated': False, 'MaChiTiet': row.ID, 'TenMon': row.TenMon, 'SoLuong': row.SoLuong,
                     'SoBan': row.SoBan, 'GhiChu': row.GhiChu, 'ThoiGian': row.ThoiGianTao.strftime('%H:%M')})

        sql_cooking = text("""
            SELECT cp.ID, m.TenMon, cp.SoLuong, h.SoBan, cp.GhiChu, p.ThoiGianTao
            FROM chitietphieugoi cp
            JOIN phieugoi p ON cp.MaPhieu = p.MaPhieu
            JOIN hoadon h ON p.MaHoaDon = h.MaHoaDon
            JOIN monan m ON cp.MaMon = m.MaMon
            WHERE cp.TrangThai = 'DangCheBien'
            ORDER BY p.ThoiGianTao ASC
        """)
        result_cooking = db.session.execute(sql_cooking).fetchall()
        for row in result_cooking:
            cooking_list.append({'MaChiTiet': row.ID, 'TenMon': row.TenMon, 'SoLuong': row.SoLuong, 'SoBan': row.SoBan,
                                 'GhiChu': row.GhiChu, 'ThoiGian': row.ThoiGianTao.strftime('%H:%M')})

        return render_template('kitchen.html', waiting_list=waiting_list, cooking_list=cooking_list, mode=mode,
                               user=session.get('fullname'), avatar_url=session.get('avatar'))
    except Exception as e:
        return f"Lỗi truy vấn: {str(e)}"