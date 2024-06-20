from collections import defaultdict
import json
from urllib.parse import parse_qs

from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt

from .forms import ListItemUpdateForm
from .models import Event, ListName, ListItem

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


def list_view_items(request):
    lists = defaultdict(list)
    all_list_items = ListItem.objects.select_related('list_name').all()
    for item in all_list_items:
        lists[item.list_name].append(item)
    context = {
        'lists': lists.items(),
    }
    return render(request, "list_main_view.html", context)

def list_update_item(request, pk):
    item = get_object_or_404(ListItem, pk=pk)
    if request.method == "PUT":
        body_data = parse_qs(request.body.decode())
        data = {key: value[0] for key, value in body_data.items()}
        form = ListItemUpdateForm(data, instance=item)
        if form.is_valid():
            item = form.save()
            return render(request, "list_item.html", {"item": item})
        else:
            return JsonResponse({"success": False, "errors": form.errors}, status=400)
    else:
        # GET request
        form = ListItemUpdateForm(instance=item)
    return render(request, "list_update_item.html", {"form": form, "item": item, "csrf_token": get_token(request)})

def list_add_item(request):
    list_id = request.POST.get('list_id')
    content = request.POST.get('content')
    if not list_id or not content:
        # TODO: this will inner swapped/replaced,
        # how to better handle errors in htmx?
        return JsonResponse(
            {"success": False, "error": "List ID and content are required"})

    try:
        list_id = int(list_id)
        list_name = ListName.objects.get(pk=list_id)
    except ListName.DoesNotExist:
        return JsonResponse(
            {"success": False, "error": "List ID does not exist"})

    # list_name should be the ListName object (not the ID)
    item = ListItem.objects.create(content=content, list_name=list_name)
    print(item)
    return render(request, "list_item.html", {"item": item})
