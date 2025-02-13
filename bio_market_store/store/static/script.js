let quantities = {};

function updateQuantity(productId, change) {
    fetch(`/update_cart/${productId}/${change}/`, {
        method: 'GET',
        headers: {
            'X-Requested-With': 'XMLHttpRequest',
        },
    })
    .then(response => response.json())
    .then(data => {
        // Update the displayed quantity
        document.getElementById(`quantity-${productId}`).textContent = data.quantity;

        // Update the quantities object
        quantities[productId] = data.quantity;

        // Update the total price
        updateTotalPrice();
    })
    .catch(error => console.error('Error:', error));
}

function updateTotalPrice() {
    let total = 0;

    // Loop through all product rows
    document.querySelectorAll('tbody tr').forEach(row => {
        const productId = row.querySelector('span').id.split('-')[1];
        const price = parseFloat(row.getAttribute('data-price'));
        const quantity = quantities[productId] || 0;

        total += price * quantity;
    });

    // Update the total price display
    document.getElementById('total-price').textContent = total.toFixed(2);
}