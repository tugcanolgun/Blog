# Generated by Django 2.2.6 on 2019-10-26 20:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [("panel", "0006_auto_20190222_1350")]

    operations = [
        migrations.AddField(
            model_name="categories",
            name="is_static_url",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="content",
            name="is_static_url",
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name="static",
            name="is_static_url",
            field=models.BooleanField(default=False),
        ),
    ]