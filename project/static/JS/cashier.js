let currentBillData = null;
let currentMaHoaDon = null;

function formatCurrency(amount) {
    return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(amount);
}

function parseCurrency(value) {
    if (!value) return 0;
    return parseFloat(value.toString().replace(/\D/g, '')) || 0;
}

$(document).ready(function() {
    $('#customer_cash').on('input', function() {
        calculateChange();
    });

    $('#customer_cash').on('blur', function() {
        const rawValue = parseCurrency($(this).val());
        if (rawValue > 0) {
            $(this).val(rawValue.toLocaleString('vi-VN'));
        }
    });

    $('#customer_cash').on('focus', function() {
        const rawValue = parseCurrency($(this).val());
        if (rawValue > 0) {
            $(this).val(rawValue);
        } else {
            $(this).val('');
        }
    });
});

function calculateChange() {
    const cashInputFormatted = $('#customer_cash').val();
    const cashInput = parseCurrency(cashInputFormatted);
    const totalAmount = parseFloat($('#summary_total').data('total')) || 0;
    let changeExact = cashInput - totalAmount;

    if(changeExact < 0) {
        $('#change_amount_display').text('Thiếu ' + formatCurrency(Math.abs(changeExact)));
        $('#change_amount_display').addClass('text-danger').removeClass('text-success');
        $('#btn_checkout').prop('disabled', true);
    } else {
        $('#change_amount_display').text(formatCurrency(changeExact));
        $('#change_amount_display').addClass('text-success').removeClass('text-danger');
        $('#change_amount').val(changeExact);

        if (totalAmount > 0) {
            $('#btn_checkout').prop('disabled', false);
        }
    }
}

function fetchBill() {
    const soBan = $('#select_table').val();

    $('#bill_items').html('<tr><td colspan="4" class="text-center text-muted py-5"><i class="fas fa-spinner fa-spin"></i> Đang tải dữ liệu...</td></tr>');
    $('#summary_total').data('total', 0).text('0 VNĐ');
    $('#customer_cash').val('');
    $('#change_amount_display').text('0 VNĐ');
    $('#btn_checkout').prop('disabled', true);

    currentBillData = null;

    if (!soBan) {
        $('#bill_items').html('<tr><td colspan="4" class="text-center text-muted py-5"><i class="fas fa-utensils"></i><br>Vui lòng chọn bàn</td></tr>');
        return;
    }

    $.get(`/api/get-bill/${soBan}`, function(response) {
        if (response.success) {
            currentBillData = response;
            currentMaHoaDon = response.ma_hoa_don;

            $('#bill_id').text('#' + response.ma_hoa_don);
            $('#time_in').text(response.thoi_gian_vao);

            let itemsHtml = '';
            response.items.forEach(item => {
                itemsHtml += `
                    <tr>
                        <td class="ps-4 fw-bold text-dark">${item.ten_mon}
                            ${item.ghi_chu ? '<br><small class="text-muted fst-italic fw-normal"><i class="fas fa-pen-alt me-1"></i>' + item.ghi_chu + '</small>' : ''}
                        </td>
                        <td class="text-center align-middle"><span class="badge bg-light text-dark border px-2">x${item.so_luong}</span></td>
                        <td class="text-end align-middle">${formatCurrency(item.don_gia)}</td>
                        <td class="text-end align-middle pe-4 fw-bold" style="color: #333;">${formatCurrency(item.thanh_tien)}</td>
                    </tr>
                `;
            });
            $('#bill_items').html(itemsHtml);

            const calcs = response.calculations;
            $('#summary_quantity').text(calcs.tong_so_luong);
            $('#summary_subtotal').text(formatCurrency(calcs.tam_tinh));
            $('#summary_vat').text(formatCurrency(calcs.vat));
            $('#summary_discount').text(formatCurrency(calcs.giam_gia));
            $('#summary_total').text(formatCurrency(calcs.tong_thanh_toan)).data('total', calcs.tong_thanh_toan);
            calculateChange();

        } else {
            $('#select_table').val('');
            $('#bill_items').html('<tr><td colspan="4" class="text-center text-muted py-5">' + response.msg + '</td></tr>');
            alert('⚠️ ' + response.msg);
        }
    });
}

function checkout() {
    const totalAmount = parseFloat($('#summary_total').data('total'));
    if (!currentMaHoaDon || totalAmount <= 0) {
        alert('Vui lòng chọn bàn có hóa đơn hợp lệ để thanh toán.');
        return;
    }
    if (!confirm(`Xác nhận thanh toán HĐ #${currentMaHoaDon} cho Bàn ${currentBillData.so_ban}?`)) {
        return;
    }
    $('#btn_checkout').prop('disabled', true).html('<i class="fas fa-spinner fa-spin"></i> Đang xử lý...');

    const postData = {
        ma_hoa_don: currentMaHoaDon,
        tong_thanh_toan: totalAmount,
        tien_khach_dua: parseFloat($('#customer_cash').val().replace(/\./g, '').replace(/,/g, '')) || 0,
        giam_gia: currentBillData.calculations.giam_gia
    };

    $.ajax({
        url: '/api/checkout',
        type: 'POST',
        contentType: 'application/json',
        data: JSON.stringify(postData),
        success: function(response) {
            if (response.success) {
                alert(`✅ Thanh toán thành công! Bàn ${currentBillData.so_ban} đã trống.`);
                window.location.reload();
            } else {
                alert('❌ Lỗi thanh toán: ' + response.msg);
                $('#btn_checkout').prop('disabled', false).html('<i class="fas fa-check-circle me-2"></i> Xác nhận Thanh toán');
            }
        },
        error: function() {
            alert('❌ Lỗi kết nối máy chủ.');
            $('#btn_checkout').prop('disabled', false).html('<i class="fas fa-check-circle me-2"></i> Xác nhận Thanh toán');
        }
    });
}