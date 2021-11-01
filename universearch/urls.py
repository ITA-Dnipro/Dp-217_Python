from django.urls import path
from . import views


urlpatterns = [
    path('', views.uni_search),
    path('<str:spec>', views.uni_search),
    path('region-data/', views.get_json_regions_data),
    path('cities-data/<str:region>/', views.get_json_cities_data),
    path('fields-data/', views.get_json_fields_data),
    path('specialities-data/<str:field>/', views.get_json_specs_data),
    path('universities/', views.get_universities),
]
