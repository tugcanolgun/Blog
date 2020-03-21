import logging

from django.shortcuts import render, get_object_or_404

from panel.models import Content, Categories, Static

logger = logging.getLogger(__name__)


def index(request):
    posts = Content.objects.order_by("-updated_at").filter(published=True).all()[:3]
    content = {"posts": posts}
    logger.info("Index page is requested", request)
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
    logger.info("All posts are requested", request)
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
    logger.info("Categories are requested", request)
    return render(request, "blog/category.html", content)


def preview(request, pk=None):
    obj = get_object_or_404(Content, id=pk)
    content = {"post": obj}
    logger.info("Preview %s is requested", obj.title, request)
    return render(request, "blog/view.html", content)


def view(request, pk=None):
    obj = get_object_or_404(Content, slug=pk)
    content = {"post": obj}
    logger.info("Content %s is requested", obj.title, request)
    return render(request, "blog/view.html", content)


def static(request, pk=None):
    obj = get_object_or_404(Static, slug=pk)
    content = {"post": obj}
    logger.info("Static page %s is requested", obj.title, request)
    return render(request, "blog/view.html", content)


def handler404(request, exception, template_name="404.html"):
    return {}
