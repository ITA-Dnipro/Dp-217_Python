from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib import messages
from .forms import CustomUserCreationForm
from .models import CustomUser
from questioning.services import get_decoded_user_results, make_top_n_results


def profile_view(request):
    user = CustomUser.objects.get(id=request.user.id)
    results = get_decoded_user_results(user)
    make_top_n_results(results)
    return render(request, 'users/profile.html', {'user': user, 'results': results})


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
