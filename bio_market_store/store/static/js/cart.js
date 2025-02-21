document.addEventListener('DOMContentLoaded', function () {
    const urlParams = new URLSearchParams(window.location.search);
    if (urlParams.has('show_cart')) {
        const cartModal = new bootstrap.Modal(document.getElementById('cartModal'));
        cartModal.show();
    }

    document.body.addEventListener('click', function (e) {
        const button = e.target.closest('.increment-btn, .decrement-btn');
        if (!button) return;

        e.preventDefault();
        const productId = button.dataset.productId;
        const url = button.dataset.url

        fetch(url)
            .then(response => response.json())
            .then(data => {
                if(data.error) {
                    console.error(error)
                    return;
                }

                document.getElementById(`quantity-${productId}`).textContent = data.quantity;
                document.getElementById(`total-${productId}`).textContent = data.total + ' zł';
                document.getElementById('cart-total').textContent = data.cart_total;
                document.querySelectorAll('.badge').forEach(badge => badge.textContent = data.total_items);
            })
            .catch(error => console.error("Error updating cart:", error));
    });
});
