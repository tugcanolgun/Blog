import random
import string
import uuid

from django.db import models
from django.template.defaultfilters import slugify


class Category(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=50, unique=True, null=False)
    created_at = models.DateField("date created", auto_now=True)
    slug = models.SlugField(default=uuid.uuid4)
    is_static_url = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        def generate_slug(name: str) -> bool:
            if Category.objects.filter(slug=name).exists():
                return True
            return False

        if self.slug is None or not self.is_static_url:
            name: str = slugify(self.name)
            while generate_slug(name=name):
                name = slugify(self.name + "-" + random.choice(string.ascii_letters))

            self.slug = name
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Static(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    title = models.CharField(max_length=50, null=False)
    body = models.TextField(null=True, default="")
    created_at = models.DateTimeField("date published")
    updated_at = models.DateTimeField("date updated", auto_now=True)
    slug = models.SlugField(default=uuid.uuid4)
    is_static_url = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        def generate_slug(title: str) -> bool:
            if Static.objects.filter(slug=title).exists():
                return True
            return False

        if self.slug is None or not self.is_static_url:
            title: str = slugify(self.title)
            while generate_slug(title=title):
                title = slugify(self.title + "-" + random.choice(string.ascii_letters))

            self.slug = title
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title


class Content(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    title = models.CharField(max_length=50, null=False)
    body = models.TextField(null=True, default="")
    published = models.BooleanField(default=False)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField("date published")
    updated_at = models.DateTimeField("date updated", auto_now=True)
    slug = models.SlugField(default=uuid.uuid4)
    is_static_url = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        def generate_slug(title: str) -> bool:
            if Content.objects.filter(slug=title).exists():
                return True
            return False

        if self.slug is None or not self.is_static_url:
            title: str = slugify(self.title)
            while generate_slug(title=title):
                title = slugify(self.title + "-" + random.choice(string.ascii_letters))

            self.slug = title
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title
