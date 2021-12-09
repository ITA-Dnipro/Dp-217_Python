from django.urls import path, include
from . import views as users_views


urlpatterns = [
    path('', users_views.profile_view, name='profile'),
    path('', include('django.contrib.auth.urls')),
    path('registration', users_views.registration_view, name='registration'),
    path('update', users_views.update_view, name='update'),
    path('add_favourite/<str:id>/', users_views.add_favourite, name='add_favourite'),
    path('remove_favourite/<str:id>/', users_views.remove_favourite, name='remove_favourite'),
]
