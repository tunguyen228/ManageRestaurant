function updateStatusSingle(id, status, btnElement) {
    // Hiệu ứng loading
    if(btnElement) {
        btnElement.innerHTML = '<i class="fas fa-circle-notch fa-spin"></i> Đang xử lý...';
        btnElement.disabled = true;
    }

    fetch('/api/cap-nhat-mon', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({type: 'single', id: id, status: status})
    })
    .then(r => r.json())
    .then(data => {
        if(data.success) {
            location.reload();
        } else {
            alert("Lỗi: " + data.msg);
            // Reset nút nếu lỗi
            if(btnElement) {
                btnElement.disabled = false;
                btnElement.innerText = "Thử lại";
            }
        }
    })
    .catch(err => {
        console.error(err);
        alert("Lỗi kết nối server!");
        if(btnElement) btnElement.disabled = false;
    });
}

function updateStatusGroup(ids, status, btnElement) {
    if(btnElement) {
        btnElement.innerHTML = '<i class="fas fa-circle-notch fa-spin"></i> Đang xử lý...';
        btnElement.disabled = true;
    }

    fetch('/api/cap-nhat-mon', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({type: 'group', ids: ids, status: status})
    })
    .then(r => r.json())
    .then(data => {
        if(data.success) {
            location.reload();
        } else {
            alert("Lỗi: " + data.msg);
            if(btnElement) {
                btnElement.disabled = false;
                btnElement.innerText = "Thử lại";
            }
        }
    })
    .catch(err => {
        console.error(err);
        alert("Lỗi kết nối server!");
        if(btnElement) btnElement.disabled = false;
    });
}
setInterval(() => {
    location.reload();
}, 30000);