from django.shortcuts import render, get_object_or_404

# from django.contrib.auth.decorators import login_required
from panel.models import Content, Categories, Static


def index(request):
    posts = Content.objects.order_by("-updated_at").filter(published=True).all()[:3]
    content = {"posts": posts}
    return render(request, "blog/index.html", content)


def allposts(request):
    # categories = Categories.objects.all()
    cont: dict = {}
    posts = (
        Content.objects.order_by("-created_at", "category").filter(published=True).all()
    )
    for post in posts:
        if post.category not in cont:
            cont[post.category] = []
        cont[post.category].append(post)
    content = {
        # 'categories': categories,
        # 'posts': posts
        "content": cont
    }
    return render(request, "blog/allposts.html", content)


def category(request, pk=None):
    obj = get_object_or_404(Categories, id=pk)
    posts = (
        Content.objects.filter(category=pk)
        .filter(published=True)
        .order_by("-updated_at")
        .all()
    )
    content = {"posts": posts, "category": obj}
    return render(request, "blog/category.html", content)


def preview(request, pk=None):
    obj = get_object_or_404(Content, id=pk)
    content = {"post": obj}
    return render(request, "blog/view.html", content)


def view(request, pk=None):
    obj = get_object_or_404(Content, slug=pk)
    content = {"post": obj}
    return render(request, "blog/view.html", content)


def static(request, pk=None):
    obj = get_object_or_404(Static, slug=pk)
    content = {"post": obj}
    return render(request, "blog/view.html", content)
