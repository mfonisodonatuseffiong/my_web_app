document.addEventListener('DOMContentLoaded', () => {
    // Select all buttons with the class 'btn-add-to-cart'
    const addToCartButtons = document.querySelectorAll('.btn-add-to-cart');
    
    addToCartButtons.forEach(button => {
        button.addEventListener('click', event => {
            event.preventDefault(); // Prevent default anchor behavior
            
            // Get the product ID from the button's data attribute
            const productId = button.getAttribute('data-product-id');
            
            // Make an HTTP POST request to add the item to the cart
            fetch(`/add_to_cart/${productId}`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-Requested-With': 'XMLHttpRequest'
                },
                // Include any additional data needed for the request
                body: JSON.stringify({ productId: productId })
            })
            .then(response => response.json()) // Parse JSON response
            .then(result => {
                if (result.success) {
                    alert('Item added to cart');
                } else {
                    alert('Failed to add item to cart');
                }
            })
            .catch(error => {
                console.error('Error:', error);
                alert('An error occurred while adding the item to the cart');
            });
        });
    });
});
