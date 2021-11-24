from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse, HttpResponseRedirect
from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser
from questioning.services import get_decoded_user_results, make_top_n_results
from universearch.services import get_universities
from enrollment_assistant.services import produce_message


def profile_view(request, update_form=None):
    user = CustomUser.objects.get(id=request.user.id)
    results = get_decoded_user_results(user)
    favourite_univers = get_universities(user.favourites)
    make_top_n_results(results)
    if not update_form:
        update_form = CustomUserChangeForm(instance=request.user)
    return render(
        request,
        template_name='users/profile.html',
        context={
            'user': user,
            'results': results,
            'update_form': update_form,
            'favourite_univers': favourite_univers
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


@login_required
def favourites(request, id):
    user = CustomUser.objects.get(id=request.user.id)
    if id in user.favourites:
        user.favourites.remove(id)
        produce_message(topic='send_email',
                        partition={'user_email': user.email,
                                   'subject': 'Enrollment assistant - Favourites',
                                   'message': f'Унiверситет {id} видалено зi списку збережених унiверситетiв'})
    else:
        user.favourites.append(id)
        produce_message(topic='send_email',
                        partition={'user_email': user.email,
                                   'subject': 'Enrollment assistant - Favourites',
                                   'message': f'Унiверситет {id} додано до списку збережених унiверситетiв'})
        messages.success(request, 'Унiверситет збережено')
    user.save()
    return HttpResponseRedirect(request.META['HTTP_REFERER'])
