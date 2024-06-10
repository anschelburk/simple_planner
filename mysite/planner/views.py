from .forms import ListForm
from .models import Event, ListItem
from django.http import HttpResponse, JsonResponse
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
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

def editable_list(request):
    if request.method == 'POST':
        new_text = request.POST.get('text', '')
        lines = new_text.split('\n')
        return JsonResponse({'lines': lines})
    return JsonResponse({'error': 'Invalid request'}, status=400)

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

def list_view(request):
    items = ListItem.objects.all()
    return render(request, 'editable_list.html', {'items': items})

def list_edit(request, item_id):
    item = get_object_or_404(ListItem, id=item_id)
    if request.method == 'POST':
        form = ListForm(request.POST, instance=item)
        if form.is_valid():
            item = form.save()
            return HttpResponse(item.name)  # Return the updated item name
    else:
        form = ListForm(instance=item)
    return render(request, 'list_item_edit.html', {'form': form, 'item': item})

def list_add(request):
    if request.method == 'POST':
        form = ListForm(request.POST)
        if form.is_valid():
            item = form.save()
            # Use render_to_string to render the URL with context
            li_content = render_to_string('list_item.html', {'item': item})
            return HttpResponse(li_content)
    else:
        form = ListForm()
    return render(request, 'editable_list_add.html', {'form': form})
