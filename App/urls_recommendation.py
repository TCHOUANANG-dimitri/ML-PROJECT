from django.urls import path
from .views_recommendation import recommendation_view

urlpatterns = [
    path("recommendation/", recommendation_view, name="recommendation"),
]
