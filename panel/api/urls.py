from django.urls import path

from panel.api import views

urlpatterns = [
    path("content/", views.ContentList.as_view(), name="content"),
]
