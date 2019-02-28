import uuid
import datetime
from django.db import models
from django.template.defaultfilters import slugify


class Categories(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=50, null=False)
    created_at = models.DateField('date created', auto_now=True)
    slug = models.SlugField(default=uuid.uuid4)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name + "-" + str(self.id)[0:2])
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Static(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    title = models.CharField(max_length=50, null=False)
    body = models.TextField(null=True, default="")
    created_at = models.DateTimeField('date published')
    updated_at = models.DateTimeField('date updated', auto_now=True)
    slug = models.SlugField(default=uuid.uuid4)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title + "-" + str(self.id)[0:2])
        super().save(*args, **kwargs)

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
    slug = models.SlugField(default=uuid.uuid4)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.title + "-" + str(self.id)[0:2])
        super().save(*args, **kwargs)

    def __str__(self):
        return self.title

    @property
    def is_published_today(self):
        return datetime.date.today == self.created_at

    @property
    def is_updated(self):
        print(self.created_at, self.updated_at, type(self.updated_at), self.updated_at.date())
        return self.created_at.date() == self.updated_at.date()



class Tags(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    name = models.CharField(max_length=50, null=False)
    created_at = models.DateField('date created', auto_now=True)


class ContentTags(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    content = models.ForeignKey(Content, on_delete=models.CASCADE)
    tag = models.ForeignKey(Tags, on_delete=models.CASCADE)
