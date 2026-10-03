async function loadProductDetail() {
    const productResponse = await fetch(`/api/products/${PRODUCT_ID}/`);
    const product = await productResponse.json();
    document.getElementById("product-name").textContent = product.name;

    const historyResponse = await fetch(`/api/products/${PRODUCT_ID}/history/`);
    const data = await historyResponse.json();

    document.getElementById("current-price").textContent = data.current_price;
    document.getElementById("lowest-price").textContent = data.lowest_price;
    document.getElementById("highest-price").textContent = data.highest_price;
    document.getElementById("price-change").textContent = data.price_change;

    drawChart(data.history);

    const comparisonResponse = await fetch(`/api/products/${PRODUCT_ID}/comparison/`);
    const comparisonData = await comparisonResponse.json();
    renderComparison(comparisonData.comparison);
}

function drawChart(history) {
    const labels = history.map(record => new Date(record.collected_at).toLocaleString());
    const prices = history.map(record => record.price);

    const ctx = document.getElementById("price-chart").getContext("2d");
    new Chart(ctx, {
        type: "line",
        data: {
            labels: labels,
            datasets: [{
                label: "Price (₹)",
                data: prices,
                borderColor: "blue",
                fill: false,
            }],
        },
    });
}

function renderComparison(comparison) {
    const tbody = document.getElementById("comparison-body");
    tbody.innerHTML = "";

    const lowestPrice = Math.min(...comparison.map(c => c.price));

    comparison.forEach(entry => {
        const row = document.createElement("tr");
        const isBest = entry.price === lowestPrice;
        row.innerHTML = `
            <td>${entry.store}</td>
            <td>${entry.price} ${isBest ? "← Best Price" : ""}</td>
        `;
        tbody.appendChild(row);
    });
}

loadProductDetail();