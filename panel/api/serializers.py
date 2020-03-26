import uuid
from typing import Optional

from django.utils import timezone
from django.db.utils import IntegrityError
from rest_framework import serializers

from panel.models import Content, Category, Static
from panel.exceptions import ValidationError


class CategorySerializer(serializers.Serializer):
    name = serializers.CharField(required=True, allow_blank=False, max_length=50)
    created_at = serializers.DateField(required=False, default=timezone.now())
    slug = serializers.SlugField(required=False, default=uuid.uuid4)
    is_static_url = serializers.BooleanField(required=False, default=False)

    def create(self, validated_data):
        """
        Create and return a new `Content` instance, given the validated data.
        """
        try:
            return Category.objects.create(**validated_data)
        except IntegrityError as exp:
            raise ValidationError(exp)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Content` instance, given the validated data.
        """
        instance.name = validated_data.get("name", instance.name)
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
    category = CategorySerializer(required=False,)
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
            if category is not None:
                validated_data["category"] = category
            else:
                raise ValidationError(f"Category does not exist")

        try:
            return Content.objects.create(**validated_data)
        except IntegrityError as exp:
            raise serializers.ValidationError(exp)

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
            if category is not None:
                instance.category = category
            else:
                raise serializers.ValidationError(f"Category does not exist")

        instance.created_at = validated_data.get("created_at", instance.created_at)
        instance.slug = validated_data.get("slug", instance.slug)
        instance.is_static_url = validated_data.get(
            "is_static_url", instance.is_static_url
        )
        instance.save()
        return instance


class StaticSerializer(serializers.Serializer):
    id = serializers.UUIDField(read_only=True)
    title = serializers.CharField(required=True, allow_blank=False, max_length=50)
    body = serializers.CharField(required=False)
    created_at = serializers.DateTimeField(required=False, default=timezone.now())
    updated_at = serializers.DateTimeField(required=False, read_only=True)
    slug = serializers.SlugField(required=False, default=uuid.uuid4)
    is_static_url = serializers.BooleanField(required=False, default=False)

    def create(self, validated_data):
        """
        Create and return a new `Content` instance, given the validated data.
        """
        try:
            return Static.objects.create(**validated_data)
        except IntegrityError as exp:
            raise serializers.ValidationError(exp)

    def update(self, instance, validated_data):
        """
        Update and return an existing `Content` instance, given the validated data.
        """
        instance.title = validated_data.get("title", instance.title)
        instance.body = validated_data.get("body", instance.body)
        instance.created_at = validated_data.get("created_at", instance.created_at)
        instance.slug = validated_data.get("slug", instance.slug)
        instance.is_static_url = validated_data.get(
            "is_static_url", instance.is_static_url
        )
        instance.save()
        return instance
