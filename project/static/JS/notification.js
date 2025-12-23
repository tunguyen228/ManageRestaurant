const notiSound = new Audio("https://actions.google.com/sounds/v1/alarms/beep_short.ogg");
let lastCount = 0;

async function syncNotifications() {
    try {
        const res = await fetch('/api/get-notifications');
        const data = await res.json();
        const count = data.length;
        const badge = document.getElementById('notiBadge');

        if (badge) {
            badge.innerText = count;
            badge.style.display = count > 0 ? 'flex' : 'none';
        }

        if (count > lastCount) {
            notiSound.play().catch(() => {
                console.log("Autoplay blocked: User needs to interact with the page first.");
            });

            if (data.length > 0) {
                showToast(data[0].msg);
            }
        }

        lastCount = count;
    } catch (err) {
    }
}

function showToast(msg) {
    const container = document.getElementById('toastContainer');
    if (!container) return;

    const html = `
        <div class="toast show align-items-center text-white bg-success border-0 mb-2 shadow" role="alert" aria-live="assertive" aria-atomic="true" style="animation: fadeIn 0.5s">
            <div class="d-flex">
                <div class="toast-body fw-bold">
                    <i class="fas fa-check-circle me-2"></i> ${msg}
                </div>
                <button type="button" class="btn-close btn-close-white me-2 m-auto" data-bs-dismiss="toast" aria-label="Close"></button>
            </div>
        </div>`;

    container.insertAdjacentHTML('beforeend', html);

    const newToast = container.lastElementChild;
    setTimeout(() => {
        if (newToast) newToast.remove();
    }, 5000);
}

function markAsRead() {
    fetch('/api/read-notifications', { method: 'POST' })
        .then(r => r.json())
        .then(d => {
            if (d.success) {
                lastCount = 0;
                syncNotifications();

                const container = document.getElementById('toastContainer');
                if(container) container.innerHTML = '';
            }
        });
}

setInterval(syncNotifications, 3000);
document.addEventListener('DOMContentLoaded', syncNotifications);
document.body.addEventListener('click', function unlockAudio() {
    notiSound.play().then(() => {
        notiSound.pause();
        notiSound.currentTime = 0;
    }).catch(() => {});
    document.body.removeEventListener('click', unlockAudio);
}, { once: true });