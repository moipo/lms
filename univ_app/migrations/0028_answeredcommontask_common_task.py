# Generated by Django 4.1.3 on 2023-01-11 16:59

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("univ_app", "0027_remove_stgroup_student_remove_stgroup_subject_and_more"),
    ]

    operations = [
        migrations.AddField(
            model_name="answeredcommontask",
            name="common_task",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                to="univ_app.commontask",
            ),
        ),
    ]
