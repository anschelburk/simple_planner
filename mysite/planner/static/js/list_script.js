document.addEventListener('htmx:configRequest', function(event) {
    var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    event.detail.headers['X-CSRFToken'] = csrfToken;
});

document.addEventListener('htmx:configRequest', function(event) {
    if (event.detail.triggeringEvent.type === 'keydown' && event.detail.triggeringEvent.key === 'Enter') {
        var form = event.detail.triggeringEvent.target.closest('form');
        if (form) {
            event.detail.path = form.getAttribute('hx-post') || form.getAttribute('hx-put');
            event.detail.headers['HX-Trigger'] = 'enter-key-submit';
        }
    }
});

document.addEventListener('htmx:afterRequest', function(event) {
    if (event.detail.xhr && event.detail.xhr.responseURL.includes("/add_item/")) {
        var listId = event.detail.triggeringEvent.target.closest('form').querySelector('[name="list_id"]').value;
        const form = document.querySelector(`#add-item-form-${listId}`);
        form.reset();  // Clear the form for the next input
        form.querySelector('input[type="text"]').focus();  // Focus on the input field

        console.log('Item added');

    }
});

function handleEnterKey(event) {
    if (event.key === 'Enter') {
        event.preventDefault();
        event.target.closest('form').dispatchEvent(new Event('submit', { cancelable: true }));
    }
}