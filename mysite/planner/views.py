from .forms import ListItemBaseForm, ListItemUpdateForm
from .models import Event, ListItem
from django.http import HttpResponse, JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import get_object_or_404, render
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from urllib.parse import parse_qs
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

def list_view_items(request):
    # = 3 queries, can we do this in one?
    work_items = ListItem.objects.filter(category="work")
    personal_items = ListItem.objects.filter(category="personal")
    other_items = ListItem.objects.filter(category="other")

    add_form = ListItemBaseForm()
    return render(
        request,
        "list_main_view.html",
        {"work_items": work_items,
         "personal_items": personal_items,
         "other_items": other_items,
         "add_form": add_form,
         "csrf_token": get_token(request)},
    )

def list_update_item(request, pk):
    item = get_object_or_404(ListItem, pk=pk)
    if request.method == "PUT":
        body_data = parse_qs(request.body.decode())
        data = {key: value[0] for key, value in body_data.items()}
        form = ListItemUpdateForm(data, instance=item)
        if form.is_valid():
            # make sure we assign the updated values to the item variable
            item = form.save()
            # early return after updating the item, function is done
            return render(request, "list_item.html", {"item": item})
    else:
        # GET request
        form = ListItemUpdateForm(instance=item)

    return render(
        request,
        "list_update_item.html",
        {"form": form, "item": item, "csrf_token": get_token(request)},
    )

def list_add_item(request):
    form = ListItemBaseForm(request.POST)
    if form.is_valid():
        item = form.save()
        return render(request, "list_item.html", {"item": item})
    return JsonResponse({"success": False})
