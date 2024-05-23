# Generated by Django 4.1.3 on 2023-01-11 11:39

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("univ_app", "0026_answeredinfotask_infotask"),
    ]

    operations = [
        migrations.RemoveField(
            model_name="stgroup",
            name="student",
        ),
        migrations.RemoveField(
            model_name="stgroup",
            name="subject",
        ),
        migrations.AddField(
            model_name="student",
            name="st_group",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="univ_app.stgroup",
            ),
        ),
        migrations.AddField(
            model_name="subject",
            name="st_group",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="univ_app.stgroup",
            ),
        ),
    ]
