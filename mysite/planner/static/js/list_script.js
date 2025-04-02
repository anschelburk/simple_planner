// Add CSRF token to all HTMX requests
document.addEventListener('htmx:configRequest', function(event) {
    var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    event.detail.headers['X-CSRFToken'] = csrfToken;
});

// Handle Enter key press in forms to trigger HTMX requests
document.addEventListener('htmx:configRequest', function(event) {
    // Check if the triggering event was a keydown event with the Enter key
    if (event.detail.triggeringEvent.type === 'keydown' && event.detail.triggeringEvent.key === 'Enter') {
        var form = event.detail.triggeringEvent.target.closest('form');
        if (form) {
            // Set the request path to the form's hx-post or hx-put attribute
            event.detail.path = form.getAttribute('hx-post') || form.getAttribute('hx-put');
            // Add an HX-Trigger header to indicate that the Enter key was pressed
            event.detail.headers['HX-Trigger'] = 'enter-key-submit';
        }
    }
});

// Reset form and focus on input after adding an item
document.addEventListener('htmx:afterRequest', function(event) {
    // Check if the request was to add an item
    if (event.detail.xhr && event.detail.xhr.responseURL.includes("/add_item/")) {
        // Get the list ID from the form
        var listId = event.detail.triggeringEvent.target.closest('form').querySelector('[name="list_id"]').value;
        // Find the form
        const form = document.querySelector(`#add-item-form-${listId}`);
        // Reset the form
        form.reset();
        // Focus on the input field
        form.querySelector('input[type="text"]').focus();

        console.log('Item added');
    }
});
