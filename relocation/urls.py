from django.urls import path
from . import views


urlpatterns = [
    path('', views.get_housings_view_2),
    path('housings_json', views.get_housings_json),
    path('tickets', views.tickets_view),
    path('stations', views.stations_view),
]
