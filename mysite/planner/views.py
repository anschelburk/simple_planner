import json
import logging

from .forms import ListItemUpdateForm
from .models import Event, ListName, ListItem
from collections import defaultdict
from django.http import JsonResponse
from django.middleware.csrf import get_token
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from urllib.parse import parse_qs

# Get an instance of a logger
logger = logging.getLogger(__name__)

def index(request):
    lists = defaultdict(list)
    all_list_items = ListItem.objects.select_related('list_name').all()
    for item in all_list_items:
        lists[item.list_name].append(item)
    context = {
        'lists': lists.items(),
    }
    return render(request, "home.html", context)

def calendar_view(request):
    return render(request, 'calendar.html')

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
    """
    Handles updating a ListItem.

    Args:
        request: The HTTP request object.
        pk: The primary key of the ListItem to update.

    Returns:
        An HTTP response.
    """
    item = get_object_or_404(ListItem, pk=pk)

    logger.debug(f"list_update_item: Request method: {request.method}")
    logger.debug(f"list_update_item: Request headers: {request.headers}")
    logger.debug(f"list_update_item: Request body: {request.body}")

    if request.method == "PUT":
        body_data = parse_qs(request.body.decode())
        data = {key: value[0] for key, value in body_data.items()}
        logger.debug(f"list_update_item: Form data: {data}")

        form = ListItemUpdateForm(data, instance=item)
        logger.debug(f"list_update_item: Form errors: {form.errors}")

        if form.is_valid():
            logger.debug(f"list_update_item: Form is valid")
            item = form.save()
            logger.debug(f"list_update_item: Item saved: {item}")
            return render(request, "list_item.html", {"item": item})
        else:
            logger.debug(f"list_update_item: Form is invalid")
            return JsonResponse({"success": False, "errors": form.errors}, status=400)
    else:
        # GET request
        form = ListItemUpdateForm(instance=item)
    return render(request, "list_update_item.html", {"form": form, "item": item, "csrf_token": get_token(request)})

def list_add_item(request):
    """
    Handles adding a new ListItem.

    Args:
        request: The HTTP request object.

    Returns:
        An HTTP response.
    """
    list_id = request.POST.get('list_id')
    content = request.POST.get('content')

    if not list_id or not content:
        logger.error("list_add_item: List ID and content are required")
        return JsonResponse(
            {"success": False, "error": "List ID and content are required"})

    try:
        list_id = int(list_id)
        list_name = ListName.objects.get(pk=list_id)
    except ListName.DoesNotExist:
        logger.error(f"list_add_item: List ID {list_id} does not exist")
        return JsonResponse(
            {"success": False, "error": "List ID does not exist"})
    except ValueError:
        logger.error(f"list_add_item: List ID {list_id} is not an integer")
        return JsonResponse(
            {"success": False, "error": "List ID must be an integer"})

    # list_name should be the ListName object (not the ID)
    item = ListItem.objects.create(content=content, list_name=list_name)
    logger.debug(f"list_add_item: Item created: {item}")
    return render(request, "list_item.html", {"item": item})
