from django.urls import path

from panel.api import views

urlpatterns = [
    path("content/", views.ContentList.as_view(), name="content_api"),
    path("content/<uuid:pk>", views.ContentList.as_view(), name="content_api"),
    path("category/", views.CategoryList.as_view(), name="category_api"),
    path("category/<str:name>", views.CategoryList.as_view(), name="category_api"),
]
