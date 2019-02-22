from django.urls import path

from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.index, name='index'),
    path('i/<slug:pk>', views.view, name='view'),
    path('view/<uuid:pk>', views.preview, name='preview'),
    path('s/<slug:pk>', views.blog.static, name='static'),
    path('category/<uuid:pk>', views.category, name='category'),
    path('all', views.allposts, name='allposts'),
]
