import logging

# from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse
from django.contrib import messages
from django.shortcuts import get_object_or_404, render, redirect, reverse
from django.contrib.auth.decorators import login_required
from panel.models import Content, Static, Category
from panel.forms import CategoryForm

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


@login_required
def category(request, pk=None):
    obj = get_object_or_404(Category, id=pk)
    posts = Content.objects.filter(category=obj).order_by("-updated_at").all()
    form = CategoryForm(request.POST or None)
    context = {"posts": posts, "form": form, "category": obj}
    return render(request, "panel/posts.html", context)


@login_required
def statics(request):
    posts = Static.objects.order_by("-updated_at").all()
    # form = CategoryForm(request.POST or None)
    # context = {'posts': posts, 'form': form}
    context = {"posts": posts}
    return render(request, "panel/posts.html", context)


@login_required
def category_add(request):
    if request.method == "POST":
        form = CategoryForm(request.POST or None)
        if form.is_valid():
            form.save()
            messages.success(request, "Category is created")
            return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))
        messages.success(request, "Could not create category")
        return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))
    messages.success(request, "Method is not allowed")
    return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))


@login_required
def category_delete(request, pk=None):
    obj = get_object_or_404(Category, id=pk)
    if obj:
        obj.delete()
        messages.success(request, f"Category {obj.name} is deleted")
        return redirect(reverse("panel:posts"))
        return HttpResponseRedirect(request.META.get("HTTP_REFERER", "/"))
    else:
        logger.warning(f"Cateogry could not be found. ID: {pk}")
        return HttpResponse(status=404)
