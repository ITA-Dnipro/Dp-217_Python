from django.shortcuts import render, redirect
from .forms import HousingForm


def get_housings_view(request):
    try:
        form = HousingForm(request.POST)
        return render(request, 'relocation/main.html', {'form': form, 'houses': form.get_housings()})
    except TypeError as e:
        print(e)
    return redirect('/')
