# Generated by Django 2.1.4 on 2019-02-22 13:38

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [("panel", "0004_static")]

    operations = [
        migrations.AddField(
            model_name="content",
            name="slug",
            field=models.SlugField(default=uuid.uuid4),
        )
    ]
