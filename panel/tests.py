from uuid import uuid4
import pytest

from django.utils import timezone
from django.contrib.auth.models import User
from django.test import TestCase, Client
from panel.models import Categories, Content, Static


class TestCategories(TestCase):
    def setUp(self):
        Categories.objects.create(name="title1", slug="title1-slug", is_static_url=True)
        Categories.objects.create(name="title2", slug="title2-slug")
        Categories.objects.create(name="title3")
        Categories.objects.create(name="title1-slug")

    def test_categories_slug(self):
        """Test Categories slug creation"""
        title1 = Categories.objects.get(name="title1")
        title2 = Categories.objects.get(name="title2")
        title3 = Categories.objects.get(name="title3")
        title1slug = Categories.objects.get(name="title1-slug")
        self.assertEqual(title1.slug, "title1-slug")
        self.assertEqual(title2.slug, "title2")
        self.assertNotEqual(title2.slug, "title2-slug")
        self.assertEqual(title3.slug, "title3")
        self.assertNotEqual(title1slug.slug, "title1-slug")
        self.assertTrue("title1-slug-" in title1slug.slug)


class TestStatic(TestCase):
    def setUp(self):
        Static.objects.create(
            title="title1",
            slug="title1-slug",
            is_static_url=True,
            created_at=timezone.now(),
        )
        Static.objects.create(
            title="title2", slug="title2-slug", created_at=timezone.now()
        )
        Static.objects.create(title="title3", created_at=timezone.now())
        Static.objects.create(title="title1-slug", created_at=timezone.now())

    def test_categories_slug(self):
        """Test Static slug creation"""
        title1 = Static.objects.get(title="title1")
        title2 = Static.objects.get(title="title2")
        title3 = Static.objects.get(title="title3")
        title1slug = Static.objects.get(title="title1-slug")
        self.assertEqual(title1.slug, "title1-slug")
        self.assertEqual(title2.slug, "title2")
        self.assertNotEqual(title2.slug, "title2-slug")
        self.assertEqual(title3.slug, "title3")
        self.assertNotEqual(title1slug.slug, "title1-slug")
        self.assertTrue("title1-slug-" in title1slug.slug)


class TestContent(TestCase):
    def setUp(self):
        Content.objects.create(
            title="title1",
            slug="title1-slug",
            is_static_url=True,
            created_at=timezone.now(),
        )
        Content.objects.create(
            title="title2", slug="title2-slug", created_at=timezone.now()
        )
        Content.objects.create(title="title3", created_at=timezone.now())
        Content.objects.create(title="title1-slug", created_at=timezone.now())

    def test_categories_slug(self):
        """Test Content slug creation"""
        title1 = Content.objects.get(title="title1")
        title2 = Content.objects.get(title="title2")
        title3 = Content.objects.get(title="title3")
        title1slug = Content.objects.get(title="title1-slug")
        self.assertEqual(title1.slug, "title1-slug")
        self.assertEqual(title2.slug, "title2")
        self.assertNotEqual(title2.slug, "title2-slug")
        self.assertEqual(title3.slug, "title3")
        self.assertNotEqual(title1slug.slug, "title1-slug")
        self.assertTrue("title1-slug-" in title1slug.slug)


class TestViews(TestCase):
    def test_auth(self):
        c = Client()
        response = c.get("/panel/posts")
        assert response.status_code == 302, response.status_code


class TestAuthorized(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user("test", "test@testing.com", "p@ssw0rd")
        self.client.login(username="test", password="p@ssw0rd")
        self.category = Categories.objects.create(
            name="name", created_at=timezone.now()
        )
        self.content = Content.objects.create(
            title="title", body="body", created_at=timezone.now()
        )
        self.static = Static.objects.create(
            title="title", body="body", created_at=timezone.now()
        )

    def test_posts(self):
        response = self.client.get("/panel/posts")
        self.assertEqual(response.status_code, 200)

    def test_post_create(self):
        response = self.client.get("/panel/post/create")
        self.assertEqual(response.status_code, 302)
        response = self.client.get(f"/panel/post/create/{uuid4()}")
        self.assertEqual(response.status_code, 404)
        response = self.client.get(f"/panel/post/create/{self.category.id}")
        self.assertEqual(response.status_code, 302)

    def test_post_edit(self):
        response = self.client.get(f"/panel/post/edit/{uuid4()}")
        self.assertEqual(response.status_code, 404)
        response = self.client.get(f"/panel/post/edit/{self.content.id}")
        self.assertEqual(response.status_code, 200)

    def test_post_delete(self):
        response = self.client.get(f"/panel/post/delete/{self.content.id}")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")

    def test_statics(self):
        response = self.client.get(f"/panel/statics")
        self.assertEqual(response.status_code, 200)

    def test_static_create(self):
        response = self.client.get(f"/panel/static/create")
        self.assertEqual(response.status_code, 302)
        self.assertTrue("/panel/static/edit/" in response.url)

    def test_static_edit(self):
        response = self.client.get(f"/panel/static/edit/{self.static.id}")
        self.assertEqual(response.status_code, 200)

    def test_static_delete(self):
        response = self.client.get(f"/panel/static/delete/{self.static.id}")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")

    def test_category_add(self):
        response = self.client.get(f"/panel/category/add")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/")

    def test_categories(self):
        self.content.category = self.category
        self.content.save()
        response = self.client.get(f"/panel/category/{self.category.id}")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(len(response.context["posts"]), 1)

    def test_category_delete(self):
        response = self.client.get(f"/panel/category/delete/{self.category.id}")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, "/panel/posts")


@pytest.fixture
def client():
    return Client()


@pytest.mark.django_db
class TestUnauthorized:
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
    def test_posts(self, url, client):
        response = client.get(f"{url}")
        assert response.status_code == 302
        assert response.url == f"/accounts/login/?next={url}"
