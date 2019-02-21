import uuid
import datetime
from django.db import models


class Categories(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=50, null=False)
    created_at = models.DateField('date created', auto_now=True)

    def __str__(self):
        return self.name


class Static(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    title = models.CharField(max_length=50, null=False)
    body = models.TextField(null=True, default="")
    created_at = models.DateTimeField('date published')
    updated_at = models.DateTimeField('date updated', auto_now=True)

    def __str__(self):
        return self.title


class Content(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    title = models.CharField(max_length=50, null=False)
    body = models.TextField(null=True, default="")
    published = models.BooleanField(default=False)
    category = models.ForeignKey(Categories, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField('date published')
    updated_at = models.DateTimeField('date updated', auto_now=True)

    def __str__(self):
        return self.title

    @property
    def is_published_today(self):
        return datetime.date.today == self.created_at


class Tags(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=50, null=False)
    created_at = models.DateField('date created', auto_now=True)


class ContentTags(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tags, on_delete=models.CASCADE)
