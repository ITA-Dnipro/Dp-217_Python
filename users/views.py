from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.http import HttpResponse
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser
from questioning.services import get_decoded_user_results, make_top_n_results


def profile_view(request, update_form=None):
    user = CustomUser.objects.get(id=request.user.id)
    results = get_decoded_user_results(user)
    make_top_n_results(results)
    if not update_form:
        update_form = CustomUserChangeForm(instance=request.user)
    return render(
        request,
        template_name='users/profile.html',
        context={
            'user': user,
            'results': results,
            'update_form': update_form
        }
    )


def registration_view(request):
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect("/")
        messages.error(request, "Unsuccessful registration. Invalid information.")
    else:
        form = CustomUserCreationForm()
    return render(request=request, template_name="registration/registration.html", context={"form": form})


def update_view(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
        return profile_view(request, update_form=form)
    else:
        return HttpResponse(405)
