# Generated by Django 3.0.4 on 2020-03-26 17:12

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):
    atomic = False  # For sqlite < 3.2

    dependencies = [
        ("panel", "0007_add_is_static_url_to_models"),
    ]

    operations = [
        migrations.RenameModel("Categories", "Category"),
        migrations.AlterField(
            model_name="content",
            name="category",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="panel.Category",
            ),
        ),
    ]
