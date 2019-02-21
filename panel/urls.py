from django.urls import path

from . import views

app_name = 'panel'
urlpatterns = [
    path('', views.index, name='index'),
    path('posts', views.posts, name='posts'),
    path('post/create', views.post_create, name='post_create'),
    path('post/create/<uuid:pk>', views.post_create, name='post_create'),
    path('post/edit/<uuid:post_id>', views.post_edit, name='post_edit'),
    path('post/delete/<uuid:post_id>', views.post_delete, name='post_delete'),

    path('statics', views.statics, name='statics'),
    path('static/create', views.static_create, name='static_create'),
    path('static/create/<uuid:pk>', views.static_create, name='static_create'),
    path('static/edit/<uuid:static_id>', views.static_edit, name='static_edit'),
    path('static/delete/<uuid:static_id>', views.static_delete, name='static_delete'),

    path('category/add', views.category_add, name='category_add'),
    path('category/delete/<uuid:pk>', views.category_delete, name='category_delete'),
    path('category/<uuid:pk>', views.category, name='category'),
    path('statics', views.statics, name='statics'),
    # path('categories/update/<uuid:pk>', views.CategoriesUpdate.as_view(), name='categories_update'),
]