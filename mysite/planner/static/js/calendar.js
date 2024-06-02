document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'dayGridMonth',
        events: '/api/get_events/',
        editable: true,
        selectable: true,
        select: function(info) {
            var title = prompt('Enter Event Title:');
            if (title) {
                var eventData = {
                    title: title,
                    start: info.startStr,
                    end: info.endStr
                };
                axios.post('/api/create_event/', eventData)
                    .then(response => {
                        calendar.addEvent({
                            id: response.data.id,
                            title: title,
                            start: info.startStr,
                            end: info.endStr
                        });
                    })
                    .catch(error => {
                        console.error('Error creating event:', error);
                    });
            }
            calendar.unselect();
        }
    });
    calendar.render();
});    