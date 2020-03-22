from uuid import uuid4
import pytest

from django.utils import timezone
from django.test import Client

from panel.models import Categories, Content, Static
from panel.factories import (
    CategoriesFactory,
    StaticFactory,
    ContentFactory,
)


@pytest.mark.usefixtures("db")
class TestSlugFunctions:
    def test_categories_slug(self):
        """Test Categories slug creation"""
        title1 = CategoriesFactory(
            name="title1", slug="title1-slug", is_static_url=True
        )
        title2 = CategoriesFactory(name="title2", slug="title2-slug")
        title3 = CategoriesFactory(name="title3")
        title1slug = CategoriesFactory(name="title1-slug")

        assert title1.slug == "title1-slug"
        assert title2.slug == "title2"
        assert title3.slug == "title3"
        assert title1slug.slug != "title1-slug"
        assert "title1-slug-" in title1slug.slug

    def test_static_slug(self):
        """Test Static slug creation"""
        title1: Static = StaticFactory(
            title="title1",
            slug="title1-slug",
            is_static_url=True,
            created_at=timezone.now(),
        )
        title2: Static = StaticFactory(
            title="title2", slug="title2-slug", created_at=timezone.now()
        )
        title3: Static = StaticFactory(title="title3", created_at=timezone.now())
        title1slug: Static = StaticFactory(
            title="title1-slug", created_at=timezone.now()
        )

        assert title1.slug == "title1-slug"
        assert title2.slug == "title2"
        assert title2.slug != "title2-slug"
        assert title3.slug == "title3"
        assert title1slug.slug != "title1-slug"
        assert "title1-slug-" in title1slug.slug

    def test_content_slug(self):
        """Test Content slug creation"""
        title1: Content = ContentFactory(
            title="title1",
            slug="title1-slug",
            is_static_url=True,
            created_at=timezone.now(),
        )
        title2: Content = ContentFactory(
            title="title2", slug="title2-slug", created_at=timezone.now()
        )
        title3: Content = ContentFactory(title="title3", created_at=timezone.now())
        title1slug: Content = ContentFactory(
            title="title1-slug", created_at=timezone.now()
        )

        assert title1.slug == "title1-slug"
        assert title2.slug == "title2"
        assert title2.slug != "title2-slug"
        assert title3.slug == "title3"
        assert title1slug.slug != "title1-slug"
        assert "title1-slug-" in title1slug.slug


@pytest.mark.usefixtures("db")
class TestAuthorized:
    def test_posts_return_200(self, user_client: Client):
        response = user_client.get("/panel/posts")

        assert response.status_code == 200

    def test_post_create(self, user_client: Client):
        response = user_client.get("/panel/post/create")

        assert response.status_code == 302

        response = user_client.get(f"/panel/post/create/{uuid4()}")

        assert response.status_code == 404

        category: Categories = CategoriesFactory(name="name", created_at=timezone.now())

        response = user_client.get(f"/panel/post/create/{category.id}")

        assert response.status_code == 302

    def test_post_edit(self, user_client: Client):
        response = user_client.get(f"/panel/post/edit/{uuid4()}")

        assert response.status_code == 404

        content: Content = ContentFactory(
            title="title", body="body", created_at=timezone.now()
        )
        response = user_client.get(f"/panel/post/edit/{content.id}")

        assert response.status_code == 200

    def test_post_delete(self, user_client: Client):
        content: Content = ContentFactory(
            title="title", body="body", created_at=timezone.now()
        )
        response = user_client.get(f"/panel/post/delete/{content.id}")

        assert response.status_code == 302
        assert response.url == "/"

    def test_statics(self, user_client: Client):
        response = user_client.get(f"/panel/statics")

        assert response.status_code == 200

    def test_static_create(self, user_client: Client):
        response = user_client.get(f"/panel/static/create")

        assert response.status_code == 302
        assert "/panel/static/edit/" in response.url

    def test_static_edit(self, user_client: Client):
        static: Static = StaticFactory(
            title="title", body="body", created_at=timezone.now()
        )
        response = user_client.get(f"/panel/static/edit/{static.id}")

        assert response.status_code == 200

    def test_static_delete(self, user_client: Client):
        static: Static = StaticFactory(
            title="title", body="body", created_at=timezone.now()
        )
        response = user_client.get(f"/panel/static/delete/{static.id}")

        assert response.status_code == 302
        assert response.url == "/"

    def test_category_add(self, user_client: Client) -> None:
        response = user_client.get(f"/panel/category/add")

        assert response.status_code == 302
        assert response.url == "/"

    def test_categories(self, user_client: Client):
        content: Content = ContentFactory(
            title="title", body="body", created_at=timezone.now()
        )
        category: Categories = CategoriesFactory(name="name", created_at=timezone.now())
        content.category = category
        content.save()

        response = user_client.get(f"/panel/category/{category.id}")

        assert response.status_code == 200
        assert len(response.context["posts"]) == 1

    def test_category_delete(self, user_client: Client) -> None:
        category: Categories = CategoriesFactory(name="name", created_at=timezone.now())

        response = user_client.get(f"/panel/category/delete/{category.id}")

        assert response.status_code == 302
        assert response.url == "/panel/posts"


@pytest.mark.usefixtures("db")
@pytest.mark.parametrize(
    "url",
    [
        f"/panel/posts",
        f"/panel/post/create",
        f"/panel/post/create/{uuid4()}",
        f"/panel/post/edit/{uuid4()}",
        f"/panel/post/delete/{uuid4()}",
        f"/panel/statics",
        f"/panel/static/create",
        f"/panel/static/edit/{uuid4()}",
        f"/panel/static/delete/{uuid4()}",
        f"/panel/category/add",
        f"/panel/category/delete/{uuid4()}",
        f"/panel/category/{uuid4()}",
    ],
)
def test_unauthorize_access_to_protected_views(url: str, client: Client) -> None:
    response = client.get(f"{url}")

    assert response.status_code == 302
    assert response.url == f"/accounts/login/?next={url}"
