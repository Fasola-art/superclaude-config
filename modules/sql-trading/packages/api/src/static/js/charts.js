/**
 * Chart.js 차트 모듈
 */

let freightChart = null;

export function renderFreightChart(data) {
    const labels = data.map(d => d.index === 'BDI' ? 'BDI' : d.route.split(' - ')[0].substring(0, 15));
    const values = data.map(d => d.value);
    const colors = data.map(d => d.change >= 0 ? 'rgba(102, 187, 106, 0.75)' : 'rgba(239, 154, 154, 0.85)');

    const ctx = document.getElementById('freightChart').getContext('2d');

    if (freightChart) freightChart.destroy();

    freightChart = new Chart(ctx, {
        type: 'bar',
        data: {
            labels: labels,
            datasets: [{
                data: values,
                backgroundColor: colors,
                borderRadius: 4,
            }]
        },
        options: {
            responsive: true,
            maintainAspectRatio: false,
            plugins: { legend: { display: false } },
            scales: {
                y: {
                    beginAtZero: true,
                    grid: { color: 'rgba(102, 187, 106, 0.15)' },
                    ticks: { color: '#78909c', font: { size: 10 } }
                },
                x: {
                    grid: { display: false },
                    ticks: { color: '#78909c', font: { size: 9 }, maxRotation: 45 }
                }
            }
        }
    });
}
