# Generated by Django 4.1.3 on 2023-01-28 19:50

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("univ_app", "0036_answeredinfotask_was_done_alter_takentest_score"),
    ]

    operations = [
        migrations.AddField(
            model_name="answeredinfotask",
            name="related_info_task",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="univ_app.infotask",
            ),
        ),
    ]
