import datetime
from uuid import uuid4
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from panel.forms import StaticForm, CategoryForm
from panel.models import Static


@login_required
def statics(request):
    """Returns the posts"""
    posts = Static.objects.order_by("-updated_at").all()
    form = CategoryForm(request.POST or None)
    context = {"posts": posts, "form": form}
    return render(request, "panel/statics/statics.html", context)


@login_required
def static_edit(request, static_id: uuid4):
    obj = get_object_or_404(Static, id=static_id)
    form = StaticForm(request.POST or None, instance=obj)
    if request.method == "POST":
        if form.is_valid():
            post = form.save(commit=False)
            post.updated_at = datetime.datetime.now()
            post.save()
            messages.success(request, "Static post is updated")
            return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))
        messages.success(request, "Static post could not be updated")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))
    return render(
        request, "panel/statics/static_write.html", {"form": form, "post": obj}
    )


@login_required
def static_delete(request, static_id: uuid4):
    obj = get_object_or_404(Static, id=static_id)
    obj.delete()
    return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))


@login_required
def static_create(request):
    obj = Static.objects.create(
        created_at=datetime.date.today(), title="Enter a title --"
    )
    messages.success(request, "Static page is created")
    return redirect(reverse("panel:static_edit", kwargs={"static_id": obj.id}))
