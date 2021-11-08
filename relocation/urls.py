from django.urls import path
from . import views


urlpatterns = [
    path('', views.get_housings_view_2),
    path('housings_json', views.get_housings_json),
    path('tickets', views.get_tickets_view),
]
