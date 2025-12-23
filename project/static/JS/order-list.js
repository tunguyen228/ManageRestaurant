function searchOrder() {
    const text = document.getElementById('searchInput').value.toLowerCase();
    document.querySelectorAll('.order-card').forEach(card => {
        const tableNum = card.dataset.table;
        if (tableNum.includes(text)) {
            card.style.display = 'block';
        } else {
            card.style.display = 'none';
        }
    });
}

function serveDish(checkbox, id, dishName, tableNum) {
    if(checkbox.checked) {
        if(!confirm(`Xác nhận đã phục vụ món "${dishName}" cho Bàn ${tableNum}?`)) {
            checkbox.checked = false;
            return;
        }

        fetch('/api/cap-nhat-mon', {
            method: 'POST',
            headers: {'Content-Type': 'application/json'},
            body: JSON.stringify({
                type: 'single',
                id: id,
                status: 'DaPhucVu'
            })
        })
        .then(r => r.json())
        .then(data => {
            if(data.success) {
                showToast(`✅ Đã phục vụ: ${dishName}`);
                checkbox.disabled = true;
                let row = checkbox.closest('.item-row');

                if (row) {
                    row.classList.add('served');
                    row.style.opacity = '0.5';
                    row.style.textDecoration = 'line-through';
                    let statusBadge = row.querySelector('.fw-bold');
                    if(statusBadge) {
                        statusBadge.className = 'fw-bold st-served';
                        statusBadge.innerText = 'Đã phục vụ';
                    }
                }

                new Audio("https://actions.google.com/sounds/v1/cartoon/pop.ogg").play().catch(()=>{});

                setTimeout(() => {
                    let searchInput = document.getElementById('searchInput');
                    if (!searchInput || searchInput.value === "") {
                        location.reload();
                    }
                }, 1000);

            } else {
                alert("❌ Lỗi: " + data.msg);
                checkbox.checked = false;
            }
        })
        .catch(err => {
            console.error(err);
            alert("Lỗi kết nối server! Vui lòng kiểm tra lại.");
            checkbox.checked = false;
        });
    }
}

function showToast(msg) {
    const container = document.getElementById('toastContainer');
    if(!container) return;
    let html = `
        <div class="toast show align-items-center text-white bg-success border-0 mb-2 shadow">
            <div class="d-flex">
                <div class="toast-body fw-bold">
                    <i class="fas fa-check-circle me-2"></i> ${msg}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast"></button>
            </div>
        </div>`;

    container.insertAdjacentHTML('beforeend', html);
    setTimeout(() => {
        const t = document.querySelectorAll('.toast');
        if(t.length > 0) t[0].remove();
    }, 3000);
}

function markAsRead() {
    const badge = document.getElementById('notiBadge');
    if(badge) badge.innerText = '0';
}

setInterval(() => {
    let searchInput = document.getElementById('searchInput');
    if (!searchInput || searchInput.value === "") {
        location.reload();
    }
}, 15000);

setInterval(() => {
    fetch('/api/get-notifications')
        .then(r => r.json())
        .then(data => {
            const badge = document.getElementById('notiBadge');
            if (badge && data.length > 0) {
                badge.innerText = data.length;
            }
        })
        .catch(() => {});
}, 5000);