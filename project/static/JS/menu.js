let cart = {};

function addToCart(id, name, price, change) {
    if (!cart[id]) cart[id] = {name: name, price: price, qty: 0, note: ""};
    cart[id].qty += change;
    const qtyElement = document.getElementById(`qty-${id}`);

    if (cart[id].qty <= 0) {
        delete cart[id];
        if (qtyElement) qtyElement.innerText = "0";
    } else {
        if (qtyElement) qtyElement.innerText = cart[id].qty;
    }
    renderCart();
}

function updateNote(id, value) {
    if (cart[id]) cart[id].note = value;
}

function renderCart() {
    const container = document.getElementById('cart-items');
    if (!container) return;

    container.innerHTML = "";
    let total = 0;

    if (Object.keys(cart).length === 0) {
        container.innerHTML = `
            <div class="text-center mt-5">
                <i class="fas fa-utensils fa-3x mb-3 text-black-50"></i>
                <p class="text-muted">Chưa có món nào được chọn</p>
            </div>`;
    }

    for (const [id, item] of Object.entries(cart)) {
        const itemTotal = item.qty * item.price;
        total += itemTotal;

        const html = `
            <div class="cart-item">
                <div class="d-flex justify-content-between align-items-start mb-2">
                    <div>
                        <div class="cart-item-name">${item.name}</div>
                        <small class="cart-item-price">${item.price.toLocaleString()} x ${item.qty}</small>
                    </div>
                    <div class="cart-item-total">${itemTotal.toLocaleString()}</div>
                </div>
                <input type="text" class="form-control form-control-sm cart-note"
                       placeholder="Ghi chú (ít cay, không hành...)"
                       value="${item.note}"
                       oninput="updateNote(${id}, this.value)">
            </div>`;
        container.insertAdjacentHTML('beforeend', html);
    }

    const totalElement = document.getElementById('cart-total');
    if (totalElement) totalElement.innerText = total.toLocaleString();
}

function filterCategory(catId, el) {
    document.querySelectorAll('.cat-chip').forEach(e => e.classList.remove('active'));
    el.classList.add('active');

    document.querySelectorAll('.dish-card').forEach(card => {
        card.style.display = (catId === 'all' || card.dataset.category == catId) ? 'block' : 'none';
    });
}

function searchDish() {
    const text = document.getElementById('searchInput').value.toLowerCase();
    document.querySelectorAll('.dish-card').forEach(card => {
        card.style.display = card.dataset.name.includes(text) ? 'block' : 'none';
    });
}

function submitOrder() {
    const tableId = document.getElementById('selectedTable').value;

    if (!tableId) return alert("⚠️ Vui lòng chọn bàn trước!");
    if (Object.keys(cart).length === 0) return alert("⚠️ Đơn hàng trống, vui lòng chọn món!");

    const items = Object.entries(cart).map(([id, item]) => ({
        id: id,
        quantity: item.qty,
        price: item.price,
        note: item.note
    }));

    fetch('/api/luu-don-hang', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({so_ban: tableId, items: items})
    })
    .then(r => r.json())
    .then(data => {
        if (data.success) {
            alert("✅ " + data.msg);
            window.location.href = "/phucvu";
        } else {
            alert("❌ Lỗi: " + data.msg);
        }
    })
    .catch(error => {
        console.error('Error:', error);
        alert("Lỗi kết nối server!");
    });
}

// setInterval(() => {
//     location.reload();
// }, 30000);