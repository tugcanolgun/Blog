import factory
from django.utils import timezone
from django.contrib.auth.models import User

from panel.models import Category, Static, Content


class CategoryFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Category

    name = "Software"


class StaticFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Static

    title = "About me"
    created_at = factory.LazyFunction(timezone.now)


class ContentFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = Content

    title = "Title"
    created_at = factory.LazyFunction(timezone.now)


class UserFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = User

    username = "test_user"
    email = "test@tugcan.net"
    password = factory.PostGenerationMethodCall("set_password", "p@ssw0rd")
