from django.urls import path

from .views import DirectionsView, DirectionDetailView

urlpatterns = [
    path('', DirectionsView.as_view()),
    path('<str:direction>/', DirectionDetailView.as_view())
]
