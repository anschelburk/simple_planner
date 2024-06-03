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