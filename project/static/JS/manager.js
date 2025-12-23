    const API_URL = '/api/revenue-report';
    let revenueChart = null;

    function formatCurrency(amount) {
        return new Intl.NumberFormat('vi-VN', { style: 'currency', currency: 'VND' }).format(amount);
    }

    function formatDate(date) {
        const d = new Date(date);
        let month = '' + (d.getMonth() + 1);
        let day = '' + d.getDate();
        const year = d.getFullYear();
        if (month.length < 2) month = '0' + month;
        if (day.length < 2) day = '0' + day;
        return [year, month, day].join('-');
    }

    function drawCategoryChart(data) {
        const ctx = document.getElementById('categoryChart').getContext('2d');
        const labels = data.map(d => d.category);
        const revenues = data.map(d => d.revenue);

        const backgroundColors = [
            '#FF4B2B', '#FF416C', '#f39c12', '#27ae60', '#3498db', '#9b59b6', '#34495e'
        ];

        if (revenueChart) {
            revenueChart.destroy();
        }

        revenueChart = new Chart(ctx, {
            type: 'doughnut',
            data: {
                labels: labels,
                datasets: [{
                    data: revenues,
                    backgroundColor: backgroundColors,
                    borderWidth: 0,
                    hoverOffset: 10
                }]
            },
            options: {
                responsive: true,
                maintainAspectRatio: false,
                plugins: {
                    legend: {
                        position: 'right',
                        labels: { font: { family: 'Baloo 2', size: 13 }, boxWidth: 15 }
                    }
                },
                layout: { padding: 20 }
            }
        });
    }

    function displayTopDishes(data) {
        const tbody = $('#top_dishes_list');
        tbody.empty();
        if (data.length === 0) {
             tbody.append('<tr><td colspan="3" class="text-center text-muted py-4"><img src="https://cdn-icons-png.flaticon.com/512/4076/4076432.png" width="50" class="opacity-50 mb-2"><br>Chưa có dữ liệu</td></tr>');
             return;
        }

        data.forEach((dish, index) => {
            let rankClass = 'rank-other';
            let rankText = index + 1;

            if (index === 0) { rankClass = 'rank-1'; rankText = '1'; }
            else if (index === 1) { rankClass = 'rank-2'; rankText = '2'; }
            else if (index === 2) { rankClass = 'rank-3'; rankText = '3'; }

            tbody.append(`
                <tr>
                    <td><div class="rank-badge ${rankClass}">${rankText}</div></td>
                    <td class="fw-bold text-dark">${dish.dish_name}</td>
                    <td class="text-end fw-bold" style="color: var(--primary-color); font-size: 1.1rem;">${dish.quantity}</td>
                </tr>
            `);
        });
    }

    function setTodayFilter() {
        const today = formatDate(new Date());
        $('#start_date').val(today);
        $('#end_date').val(today);
        fetchReport();
    }

    function fetchReport() {
        const start_date = $('#start_date').val();
        const end_date = $('#end_date').val();

        $('#kpi_revenue').text('...');
        $('#kpi_invoices').text('...');
        $('#kpi_avg_revenue').text('...');
        $('#top_dishes_list').html('<tr><td colspan="3" class="text-center text-muted py-4"><div class="spinner-border text-danger spinner-border-sm" role="status"></div> Đang tải...</td></tr>');

        $.get(API_URL, { start_date: start_date, end_date: end_date }, function(response) {
            if (response.success) {
                const summary = response.summary;

                $('#kpi_revenue').text(formatCurrency(summary.total_revenue));
                $('#kpi_invoices').text(summary.total_invoices);
                $('#kpi_avg_revenue').text(formatCurrency(summary.avg_revenue_per_invoice));
                $('#report_period').text(summary.report_period);

                drawCategoryChart(response.category_report);
                displayTopDishes(response.top_dishes);

            } else {
                alert('⚠️ ' + response.msg);
                $('#top_dishes_list').html('<tr><td colspan="3" class="text-center text-danger py-4">Lỗi tải dữ liệu</td></tr>');
            }
        }).fail(function() {
            alert('❌ Lỗi kết nối máy chủ.');
        });
    }

    $(document).ready(function() {
        setTodayFilter();
    });