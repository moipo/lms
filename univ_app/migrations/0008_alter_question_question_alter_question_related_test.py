# Generated by Django 4.0.5 on 2022-08-19 16:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("univ_app", "0007_alter_question_question"),
    ]

    operations = [
        migrations.AlterField(
            model_name="question",
            name="question",
            field=models.TextField(default=""),
        ),
        migrations.AlterField(
            model_name="question",
            name="related_test",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="univ_app.test",
            ),
        ),
    ]
