# Generated by Django 3.0.4 on 2020-03-26 20:10

from django.db import migrations


class Migration(migrations.Migration):
    atomic = False  # For sqlite < 3.2

    dependencies = [
        ("panel", "0009_alter_name_in_category"),
    ]

    operations = [
        migrations.DeleteModel(name="ContentTags",),
        migrations.DeleteModel(name="Tags",),
    ]