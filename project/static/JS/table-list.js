let selectedTableId = null;

function confirmSelectTable(tableId, status) {
    if (status === 'DatTruoc') return alert("🚫 Bàn này ĐÃ ĐẶT TRƯỚC!");
    if (status === 'CoKhach') return alert("🚫 Bàn này ĐANG CÓ KHÁCH!");

    selectedTableId = tableId;

    const modalNum = document.getElementById('modalTableNum');
    if(modalNum) modalNum.innerText = tableId;

    const btn = document.getElementById('btnGoToMenu');
    if(btn) {
        btn.onclick = function () {
            window.location.href = "/menu?table_id=" + selectedTableId;
        };
    }

    const modalEl = document.getElementById('confirmModal');
    if(modalEl) {
        new bootstrap.Modal(modalEl).show();
    }
}