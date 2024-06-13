document.addEventListener('htmx:configRequest', function(event) {
    var csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    event.detail.headers['X-CSRFToken'] = csrfToken;
});

document.addEventListener('htmx:configRequest', function(event) {
    if (event.detail.triggeringEvent.type === 'keydown' && event.detail.triggeringEvent.key === 'Enter') {
        var listId = event.detail.triggeringEvent.target.closest('form').querySelector('[name="list_id"]').value;
        event.detail.path = `/list/${listId}/add_item/`;
        event.detail.headers['HX-Trigger'] = 'add-new-item';
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
        event.target.blur();
    }
}