from django.urls import path
from .views.user_views import create_user


urlpatterns = [
    path("create/", create_user, name="create_user"),
]