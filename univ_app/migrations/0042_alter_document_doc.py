# Generated by Django 4.1.3 on 2023-01-31 13:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("univ_app", "0041_remove_document_st_group_document_subject"),
    ]

    operations = [
        migrations.AlterField(
            model_name="document",
            name="doc",
            field=models.FileField(null=True, upload_to="uploads/documents/"),
        ),
    ]
