# Generated by Django 4.1.3 on 2023-01-31 12:27

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("univ_app", "0040_alter_student_profile_picture_and_more"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="document",
            name="st_group",
        ),
        migrations.AddField(
            model_name="document",
            name="subject",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="univ_app.subject",
            ),
        ),
    ]
