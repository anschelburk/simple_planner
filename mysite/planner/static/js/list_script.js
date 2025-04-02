// Add CSRF token to all HTMX requests
document.addEventListener('htmx:configRequest', function(event) {
    var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    event.detail.headers['X-CSRFToken'] = csrfToken;
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

// Prevent default form submission for the update item form
document.addEventListener('DOMContentLoaded', function() {
    const updateItemForm = document.getElementById('update-item-form');
    if (updateItemForm) {
        updateItemForm.addEventListener('submit', function(event) {
            event.preventDefault();
        });
    }
});
