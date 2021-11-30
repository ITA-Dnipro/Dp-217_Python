import requests
from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.conf import settings
from .forms import HousingForm, TicketsSearchForm
from .services import HousingService as Housings


def get_housings_view(request):
    try:
        form = HousingForm(request.POST)
        return render(request, 'relocation/main.html', {'form': form, 'houses': form.get_housings()})
    except TypeError as e:
        print(e)
    return redirect('/')


def get_housings_view_2(request):
    return render(request, 'relocation/main2.html')


def get_housings_json(request):
    return JsonResponse(Housings.all_json(), safe=False, json_dumps_params={'ensure_ascii': False})


def tickets_view(request):
    tickets = {}
    ui_messages = []
    if request.method == 'POST':
        form = TicketsSearchForm(request.POST)
        if form.is_valid():
            url = settings.TICKETS_SEARCH_URL
            loaded_tickets = requests.request("POST", url, data=form.to_json()).json()
            if loaded_tickets['trips']:
                tickets[form.data['type']] = loaded_tickets
            else:
                ui_messages.append("Квитки не знайдені")
    else:
        form = TicketsSearchForm()

    return render(request, 'relocation/tickets.html', {'tickets': tickets, 'form': form, 'ui_messages': ui_messages})


def get_stations(request):
    pass

