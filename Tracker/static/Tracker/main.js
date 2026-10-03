const API_BASE = "/api/products/";

async function loadProducts() {
    const response = await fetch(API_BASE);
    const products = await response.json();

    const tbody = document.getElementById("product-table-body");
    tbody.innerHTML = "";

    products.forEach(product => {
        const row = document.createElement("tr");
        row.innerHTML = `
            <td><a href="/product/${product.id}/">${product.name}</a></td>
            <td>${product.store}</td>
            <td>${product.is_active ? "Yes" : "No"}</td>
            <td>
                <button onclick="toggleActive(${product.id}, ${product.is_active})">
                    ${product.is_active ? "Disable" : "Enable"}
                </button>
                <button onclick="deleteProduct(${product.id})">Remove</button>
            </td>
        `;
        tbody.appendChild(row);
    });
}

async function addProduct(event) {
    event.preventDefault();

    const name = document.getElementById("name").value;
    const url = document.getElementById("url").value;
    const store = document.getElementById("store").value;
    const target_price = document.getElementById("target_price").value || null;

    await fetch(API_BASE, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, url, store, target_price }),
    });

    document.getElementById("add-product-form").reset();
    loadProducts();
}

async function toggleActive(id, currentStatus) {
    await fetch(`${API_BASE}${id}/`, {
        method: "PATCH",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ is_active: !currentStatus }),
    });
    loadProducts();
}

async function deleteProduct(id) {
    await fetch(`${API_BASE}${id}/`, { method: "DELETE" });
    loadProducts();
}

document.getElementById("add-product-form").addEventListener("submit", addProduct);
loadProducts();