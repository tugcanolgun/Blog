import factory
from django.utils import timezone
from django.contrib.auth.models import User

from panel.models import Categories, Static, Content


class CategoriesFactory(factory.DjangoModelFactory):
    class Meta:
        model = Categories

    name = "Software"


class StaticFactory(factory.DjangoModelFactory):
    class Meta:
        model = Static

    title = "About me"
    created_at = factory.LazyFunction(timezone.now)


class ContentFactory(factory.DjangoModelFactory):
    class Meta:
        model = Content

    title = "Title"
    created_at = factory.LazyFunction(timezone.now)


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    username = "test_user"
    email = "test@tugcan.net"
    password = factory.PostGenerationMethodCall("set_password", "p@ssw0rd")
