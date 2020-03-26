from typing import Set, Dict, Any

import pytest
from django.test import Client
from django.urls import reverse
from rest_framework import status

from panel.factories import ContentFactory, CategoryFactory
from panel.models import Content, Category


@pytest.mark.usefixtures("db")
class TestContentEndpoint:
    def test_endpoint_rejects_unauthenticated_users(self, client: Client):
        response = client.get(
            reverse("panel:content_api"),
            # content_type="application/json",
        )

        assert response.status_code == status.HTTP_403_FORBIDDEN

    def test_endpoint_returns_contents_in_db(self, user_client: Client):
        ContentFactory(
            title="Title1", body="Text", published=False, is_static_url=False
        )
        keys: Set[str] = {
            "id",
            "title",
            "body",
            "published",
            "category",
            "created_at",
            "updated_at",
            "slug",
            "is_static_url",
        }

        response = user_client.get(reverse("panel:content_api"),)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.json()) == 1
        assert keys == response.json()[0].keys()
        assert response.json()[0]["title"] == "Title1"
        assert response.json()[0]["body"] == "Text"
        assert response.json()[0]["published"] is False
        assert response.json()[0]["slug"] == "title1"
        assert response.json()[0]["is_static_url"] is False

    def test_post_creates_new_content_without_category(self, user_client: Client):
        data: Dict[str, Any] = {"title": "Title1", "body": "Body text"}
        response = user_client.post(
            reverse("panel:content_api"), data=data, content_type="application/json",
        )

        assert response.status_code == status.HTTP_201_CREATED, response.content
        assert Content.objects.count() == 1

        content: Content = Content.objects.first()

        assert content.title == data["title"]
        assert content.body == data["body"]
        assert content.slug == data["title"].lower()
        assert content.published is False
        assert content.category is None
        assert content.is_static_url is False

    def test_post_creates_new_content_with_category(self, user_client: Client):
        category: Category = CategoryFactory()
        data: Dict[str, Any] = {
            "title": "Title1",
            "body": "Body text",
            "category": {"name": category.name},
        }

        response = user_client.post(
            reverse("panel:content_api"), data=data, content_type="application/json",
        )

        assert response.status_code == status.HTTP_201_CREATED, response.content
        assert Content.objects.count() == 1
        assert Content.objects.first().category == category, category.name

    def test_post_creates_new_content_with_invalid_category(self, user_client: Client):
        data: Dict[str, Any] = {
            "title": "Title1",
            "body": "Body text",
            "category": {"name": "some_category"},
        }

        response = user_client.post(
            reverse("panel:content_api"), data=data, content_type="application/json",
        )

        assert response.status_code == status.HTTP_201_CREATED, response.content
        assert Content.objects.count() == 1
        assert Content.objects.first().category is None

    def test_patch_partially_updates_content(self, user_client: Client):
        initial_content: Content = ContentFactory(
            title="Title1", body="Text", published=False, is_static_url=False,
        )
        data: Dict[str, Any] = {
            "title": "Title2",
            "body": "Body text",
        }
        response = user_client.patch(
            reverse("panel:content_api", kwargs={"pk": str(initial_content.id)}),
            data=data,
            content_type="application/json",
        )

        assert response.status_code == status.HTTP_200_OK, response.content
        assert Content.objects.count() == 1

        content: Content = Content.objects.first()

        assert content.title == data["title"]
        assert content.body == data["body"]
        assert content.slug == data["title"].lower()
        assert content.published is False
        assert content.category is None
        assert content.is_static_url is False
        assert content.created_at == initial_content.created_at
        assert content.updated_at != initial_content.updated_at

    def test_patch_updates_category(self, user_client: Client):
        initial_category: Category = CategoryFactory()
        new_category: Category = CategoryFactory(name="Personal")
        initial_content: Content = ContentFactory(category=initial_category)
        data: Dict[str, Any] = {
            "title": "Title2",
            "body": "Body text",
            "category": {"name": new_category.name},
        }

        response = user_client.patch(
            reverse("panel:content_api", kwargs={"pk": str(initial_content.id)}),
            data=data,
            content_type="application/json",
        )

        assert response.status_code == status.HTTP_200_OK, response.content
        assert Content.objects.count() == 1
        assert Content.objects.first().category == new_category

    def test_delete_removes_content(self, user_client: Client):
        content: Content = ContentFactory()

        response = user_client.delete(
            reverse("panel:content_api", kwargs={"pk": str(content.id)}),
            content_type="application/json",
        )

        assert response.status_code == status.HTTP_204_NO_CONTENT, response.content
        assert Content.objects.count() == 0
