# Generated by Django 4.1.1 on 2022-10-01 09:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("univ_app", "0014_remove_question_importance_test_image"),
    ]

    operations = [
        migrations.AlterField(
            model_name="test",
            name="description",
            field=models.TextField(blank=True, default=""),
        ),
    ]
