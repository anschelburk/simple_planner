document.addEventListener('DOMContentLoaded', function() {
    var calendarEl = document.getElementById('calendar');
    var calendar = new FullCalendar.Calendar(calendarEl, {
        initialView: 'timeGridDay',
        events: '/api/get_events/',
        editable: true,
        selectable: true,
        select: function(info) {
            $('#eventTitle').val('');
            $('#eventStart').val(info.startStr);
            $('#eventEnd').val(info.endStr);
            $('#editEventModal').modal('show');

            $('#saveEventChanges').off('click').on('click', function() {
                var title = $('#eventTitle').val();
                var start = $('#eventStart').val();
                var end = $('#eventEnd').val();
                if (title && start && end) {
                    var eventData = {
                        title: title,
                        start: start,
                        end: end
                    };
                    axios.post('/api/create_event/', eventData)
                        .then(response => {
                            calendar.addEvent({
                                id: response.data.id,
                                title: title,
                                start: start,
                                end: end
                            });
                            $('#editEventModal').modal('hide');
                        })
                        .catch(error => {
                            console.error('Error creating event:', error);
                        });
                }
            });
            calendar.unselect();
        },
        eventClick: function(info) {
            $('#eventId').val(info.event.id);
            $('#eventTitle').val(info.event.title);
            $('#eventStart').val(info.event.start.toISOString().slice(0, 16));
            $('#eventEnd').val(info.event.end ? info.event.end.toISOString().slice(0, 16) : '');
            $('#editEventModal').modal('show');

            $('#saveEventChanges').off('click').on('click', function() {
                var id = $('#eventId').val();
                var title = $('#eventTitle').val();
                var start = $('#eventStart').val();
                var end = $('#eventEnd').val();
                if (title && start && end) {
                    var eventData = {
                        id: id,
                        title: title,
                        start: start,
                        end: end
                    };
                    axios.put('/api/update_event/', eventData)
                        .then(response => {
                            info.event.setProp('title', title);
                            info.event.setStart(start);
                            info.event.setEnd(end);
                            $('#editEventModal').modal('hide');
                        })
                        .catch(error => {
                            console.error('Error updating event:', error);
                        });
                }
            });
        },
        eventResize: function(info) {
            var eventData = {
                id: info.event.id,
                start: info.event.start.toISOString(),
                end: info.event.end ? info.event.end.toISOString() : null
            };
            axios.put('/api/update_event/', eventData)
                .then(response => {
                    console.log('Event resized successfully');
                })
                .catch(error => {
                    console.error('Error resizing event:', error);
                });
        },
        eventDrop: function(info) {
            var eventData = {
                id: info.event.id,
                start: info.event.start.toISOString(),
                end: info.event.end ? info.event.end.toISOString() : null
            };
            axios.put('/api/update_event/', eventData)
                .then(response => {
                    console.log('Event dropped successfully');
                })
                .catch(error => {
                    console.error('Error dropping event:', error);
                });
        }
    });
    calendar.render();
});
