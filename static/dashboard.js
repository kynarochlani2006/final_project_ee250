let priceChart;
let volChart;

async function fetchData() {
    const res = await fetch("/data");
    return await res.json();
}

async function updateCharts() {
    const data = await fetchData();
    const prices = data.map(d => d.price);
    const vols = data.map(d => d.volatility);
    const spikes = data.map(d => d.spike);

    if (!priceChart) {
        const ctx1 = document.getElementById("priceChart").getContext("2d");
        priceChart = new Chart(ctx1, {
            type: "line",
            data: { labels: prices.map((_, i) => i), datasets: [{ label: "Price", data: prices }] }
        });

        const ctx2 = document.getElementById("volChart").getContext("2d");
        volChart = new Chart(ctx2, {
            type: "line",
            data: { labels: vols.map((_, i) => i), datasets: [{ label: "Volatility", data: vols }] }
        });
    } else {
        priceChart.data.datasets[0].data = prices;
        volChart.data.datasets[0].data = vols;
        priceChart.update();
        volChart.update();
    }

    const lastSpike = spikes[spikes.length - 1];
    document.getElementById("alertBox").innerText = lastSpike ? "⚠️ Volatility Spike Detected!" : "";
}

setInterval(updateCharts, 1000);
