async function fetchData() {
    const res = await fetch("/data");
    return await res.json();
}

const priceCtx = document.getElementById("priceChart").getContext("2d");
const volCtx = document.getElementById("volChart").getContext("2d");

let priceChart = new Chart(priceCtx, {
    type: "line",
    data: {
        labels: [],
        datasets: [{
            label: "Price",
            data: [],
            borderColor: "#00eaff",
            backgroundColor: "rgba(0, 234, 255, 0.1)",
            tension: 0.25,
            pointRadius: 0
        }]
    },
    options: {
        scales: {
            x: { ticks: { color: "#f0f6fc" } },
            y: { ticks: { color: "#f0f6fc" } }
        },
        plugins: { legend: { labels: { color: "#f0f6fc" } } }
    }
});

let volChart = new Chart(volCtx, {
    type: "line",
    data: {
        labels: [],
        datasets: [{
            label: "Volatility",
            data: [],
            borderColor: "#ff0099",
            backgroundColor: "rgba(255, 0, 153, 0.15)",
            tension: 0.25,
            pointRadius: 0
        }]
    },
    options: {
        scales: {
            x: { ticks: { color: "#f0f6fc" } },
            y: { ticks: { color: "#f0f6fc" } }
        },
        plugins: { legend: { labels: { color: "#f0f6fc" } } }
    }
});

function updateCharts() {
    fetchData().then(data => {
        const labels = data.map(d => new Date(d.timestamp * 1000).toLocaleTimeString());
        const prices = data.map(d => d.price);
        const vols = data.map(d => d.volatility);

        priceChart.data.labels = labels;
        priceChart.data.datasets[0].data = prices;
        priceChart.update();

        volChart.data.labels = labels;
        volChart.data.datasets[0].data = vols;
        volChart.update();

        const alertBox = document.getElementById("alertBox");
        if (data.length && data[data.length - 1].spike) {
            alertBox.textContent = "⚠️ Volatility Spike Detected!";
            alertBox.style.color = "#ff0099";
            alertBox.style.borderColor = "#ff0099";
        } else {
            alertBox.textContent = "No spike detected.";
        }
    });
}

setInterval(updateCharts, 1000);
