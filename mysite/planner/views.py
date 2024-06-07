from .models import Event
from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
import json

def calendar_view(request):
    return render(request, 'calendar.html')

@csrf_exempt
def create_event(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        event = Event.objects.create(
            title=data['title'],
            start=data['start'],
            end=data['end']
        )
        return JsonResponse({'id': event.id})

def get_events(request):
    events = Event.objects.all().values('id', 'title', 'start', 'end')
    return JsonResponse(list(events), safe=False)

def editable_textbox(request):
    pass

@csrf_exempt
def update_event(request):
    if request.method == 'PUT':
        try:
            data = json.loads(request.body)
            event_id = data.get('id')
            title = data.get('title')
            start = data.get('start')
            end = data.get('end')

            # Retrieve the event from the database
            event = Event.objects.get(id=event_id)

            # Update the event fields
            event.title = title
            event.start = start
            event.end = end
            event.save()

            return JsonResponse({'status': 'success'}, status=200)
        except Event.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Event not found'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)
    else:
        return JsonResponse({'status': 'error', 'message': 'Invalid HTTP method'}, status=405)
