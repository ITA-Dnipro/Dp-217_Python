from django.urls import path
from .views import ResultViewSet, QuestioningViewSet, questioning_view

urlpatterns = [
    path('', questioning_view, name='questioning'),
    path('questions/<int:questions_type>', QuestioningViewSet.as_view()),
    path('questions/', QuestioningViewSet.as_view()),
    path('results/<slug:link>', ResultViewSet.as_view()),
    path('results/', ResultViewSet.as_view()),
    path('results/<int:id>/delete', ResultViewSet.as_view()),
]
