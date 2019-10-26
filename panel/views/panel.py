import datetime
from uuid import uuid4
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from panel.forms import BlogForm, CategoryForm
from panel.models import Content, Categories


@login_required
def index(request):
    """Index page view"""
    return render(request, "panel/index.html")


@login_required
def posts(request):
    """Returns the posts"""
    posts = Content.objects.order_by("-updated_at").all()
    form = CategoryForm(request.POST or None)
    context = {"posts": posts, "form": form}
    return render(request, "panel/posts.html", context)


@login_required
def post_edit(request, post_id: uuid4):
    obj = get_object_or_404(Content, id=post_id)
    form = BlogForm(request.POST or None, instance=obj)
    if request.method == "POST":
        if form.is_valid():
            post = form.save(commit=False)
            post.updated_at = datetime.datetime.now()
            post.save()
            messages.success(request, "Post is updated")
            return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))
        messages.success(request, "Post could not be updated")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))
    return render(request, "panel/write.html", {"form": form, "post": obj})


@login_required
def post_delete(request, post_id: uuid4):
    obj = get_object_or_404(Content, id=post_id)
    obj.delete()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))


@login_required
def post_create(request, pk=None):
    if pk:
        cat = get_object_or_404(Categories, id=pk)
    else:
        cat = None
    obj = Content.objects.create(
        created_at=datetime.date.today(), title="Enter a title --", category=cat
    )
    messages.success(request, "Category is created")
    return redirect(reverse("panel:post_edit", kwargs={"post_id": obj.id}))
