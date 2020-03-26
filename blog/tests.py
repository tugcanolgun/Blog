import pytest
from django.test import Client

from panel.models import Category, Content, Static
from panel.factories import (
    CategoryFactory,
    StaticFactory,
    ContentFactory,
)


@pytest.mark.usefixtures("db")
class TestAccessibility:
    def test_index_page(self, client: Client) -> None:
        response = client.get("/")

        assert response.status_code == 200

    def test_all_posts(self, client: Client) -> None:
        response = client.get("/all")

        assert response.status_code == 200

    def test_category(self, client: Client) -> None:
        category: Category = CategoryFactory()

        response = client.get(f"/category/{category.id}")

        assert response.status_code == 200, category.slug

    def test_static(self, client: Client) -> None:
        static: Static = StaticFactory()

        response = client.get(f"/s/{static.slug}")

        assert response.status_code == 200

    def test_preview(self, client: Client) -> None:
        content: Content = ContentFactory()

        response = client.get(f"/view/{content.id}")

        assert response.status_code == 200

    def test_content_view(self, client: Client) -> None:
        content: Content = ContentFactory()

        response = client.get(f"/i/{content.slug}")

        assert response.status_code == 200
