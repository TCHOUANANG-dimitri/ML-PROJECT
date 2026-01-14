from django.urls import path
from . import views

# Try to import recommendation_view; if it fails, the API still works
try:
    from views_recommendation import recommendation_view
    has_recommendation = True
except ImportError:
    has_recommendation = False
    recommendation_view = None

urlpatterns = [
    path("", views.index, name="index"),
    path("api/recommend/", views.api_recommend, name="api_recommend"),
    path("api/program/", views.api_program, name="api_program"),
    path("api/upload_students/", views.api_upload_students, name="api_upload_students"),
    path("api/analyze/", views.api_analyze, name="api_analyze"),
    path("api/load_resources/", views.api_load_resources, name="api_load_resources"),
    path("api/load_teachers/", views.api_load_teachers, name="api_load_teachers"),
]

if has_recommendation:
    urlpatterns.append(path("recommendation/", recommendation_view, name="recommendation"))