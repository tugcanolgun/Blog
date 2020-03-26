import uuid
from typing import Optional

from django.utils import timezone
from rest_framework import serializers

from panel.models import Content, Category


class CategorySerializer(serializers.Serializer):
    name = serializers.CharField(required=True, allow_blank=False, max_length=50)
    created_at = serializers.DateField(required=False, default=timezone.now())
    slug = serializers.SlugField(required=False, default=uuid.uuid4)
    is_static_url = serializers.BooleanField(required=False, default=False)

    def create(self, validated_data):
        """
        Create and return a new `Content` instance, given the validated data.
        """
        return Category.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Content` instance, given the validated data.
        """
        instance.name = validated_data.get("title", instance.title)
        instance.created_at = validated_data.get("created_at", instance.created_at)
        instance.slug = validated_data.get("slug", instance.slug)
        instance.is_static_url = validated_data.get(
            "is_static_url", instance.is_static_url
        )
        instance.save()
        return instance


class ContentSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    title = serializers.CharField(required=True, allow_blank=False, max_length=50)
    body = serializers.CharField(required=False)
    published = serializers.BooleanField(required=False, default=False)
    category = CategorySerializer(required=False)
    created_at = serializers.DateTimeField(required=False, default=timezone.now())
    updated_at = serializers.DateTimeField(required=False, read_only=True)
    slug = serializers.SlugField(required=False, default=uuid.uuid4)
    is_static_url = serializers.BooleanField(required=False, default=False)

    def create(self, validated_data):
        """
        Create and return a new `Content` instance, given the validated data.
        """
        if validated_data.get("category"):
            category: Optional[Category] = Category.objects.filter(
                name=validated_data["category"].get("name")
            ).first()
            if category:
                validated_data["category"] = category
            else:
                validated_data["category"] = None

        return Content.objects.create(**validated_data)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Content` instance, given the validated data.
        """
        instance.title = validated_data.get("title", instance.title)
        instance.body = validated_data.get("body", instance.body)
        instance.published = validated_data.get("published", instance.published)
        if validated_data.get("category"):
            category: Optional[Category] = Category.objects.filter(
                name=validated_data["category"].get("name")
            ).first()
            if not category:
                raise ValueError(f"Category does not exist")

            instance.category = category

        instance.created_at = validated_data.get("created_at", instance.created_at)
        instance.slug = validated_data.get("slug", instance.slug)
        instance.is_static_url = validated_data.get(
            "is_static_url", instance.is_static_url
        )
        instance.save()
        return instance
