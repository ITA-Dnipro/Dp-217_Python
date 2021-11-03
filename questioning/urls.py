from django.urls import path
from . import views

urlpatterns = [
    path('', views.questioning_view, name='questioning'),
    path('get_questions/<int:questions_type>', views.get_questions),
    path('ajax/', views.questioning_ajax, name='ajax'),
    path('results/<slug:link>', views.questioning_results),
    path('results/', views.questioning_results, name='questioning_results'),
    path('results/delete/<int:id>', views.delete_result),
]
