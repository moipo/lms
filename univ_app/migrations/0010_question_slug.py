# Generated by Django 4.0.5 on 2022-09-09 15:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("univ_app", "0009_alter_answer_related_question"),
    ]

    operations = [
        migrations.AddField(
            model_name="question",
            name="slug",
            field=models.SlugField(blank=True, max_length=400, null=True),
        ),
    ]
