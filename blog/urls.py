from django.urls import path

from . import views

app_name = 'blog'
urlpatterns = [
    path('', views.index, name='index'),
    path('view/<uuid:pk>', views.preview, name='preview'),
    path('s/<uuid:pk>', views.blog.static, name='static'),
    path('category/<uuid:pk>', views.category, name='category'),
    path('all', views.allposts, name='allposts'),
]
