// Main JavaScript
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips and popovers if using Bootstrap
    var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'))
    var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
        return new bootstrap.Tooltip(tooltipTriggerEl)
    })
});

// Helper function for AJAX calls
function sendAjax(url, method = 'GET', data = null) {
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
        }
    };
    
    if (data && method !== 'GET') {
        options.body = JSON.stringify(data);
    }
    
    return fetch(url, options)
        .then(response => response.json())
        .catch(error => console.error('Error:', error));
}

// Cart functions
function addToCart(productId, quantity = 1) {
    const form = document.createElement('form');
    form.method = 'POST';
    form.action = `/cart/add/${productId}`;
    
    const input = document.createElement('input');
    input.name = 'quantity';
    input.value = quantity;
    
    form.appendChild(input);
    document.body.appendChild(form);
    form.submit();
}

// Confirm delete
function confirmDelete(message = 'Bạn chắc chắn muốn xóa?') {
    return confirm(message);
}
