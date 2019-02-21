from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
from panel.models import Content, Categories, Static


def index(request):
    posts = Content.objects.order_by('-updated_at').filter(published=True).all()[:3]
    content = {
        'posts': posts,
        }
    return render(request, 'blog/index.html', content)


def categories(request):
    categories = Categories.objects.all()
    content = {
        'categories': categories,
        }
    return render(request, 'blog/categories.html', content)


def category(request, pk=None):
    obj = get_object_or_404(Categories, id=pk)
    posts = Content.objects.filter(category=pk).filter(published=True).order_by('-updated_at').all()
    content = {
        'posts': posts,
        'category': obj
        }
    return render(request, 'blog/category.html', content)


def preview(request, pk=None):
    print("View is requested", pk)
    obj = get_object_or_404(Content, id=pk)
    content = {'post': obj}
    return render(request, 'blog/view.html', content)


def static(request, pk=None):
    print("Static is requested", pk)
    obj = get_object_or_404(Static, id=pk)
    content = {'post': obj}
    return render(request, 'blog/view.html', content)

