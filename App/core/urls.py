from django.urls import path
from . import views
from views_recommendation import recommendation_view

urlpatterns = [
    path("", views.index, name="index"),
    path("api/recommend/", views.api_recommend, name="api_recommend"),
    path("api/program/", views.api_program, name="api_program"),
    path("api/upload_students/", views.api_upload_students, name="api_upload_students"),
    path("recommendation/", recommendation_view, name="recommendation"),
]