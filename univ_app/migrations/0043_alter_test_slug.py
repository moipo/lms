# Generated by Django 4.1.3 on 2023-02-03 18:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("univ_app", "0042_alter_document_doc"),
    ]

    operations = [
        migrations.AlterField(
            model_name="test",
            name="slug",
            field=models.SlugField(blank=True, max_length=120, null=True),
        ),
    ]
