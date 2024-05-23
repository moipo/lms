# Generated by Django 4.1.1 on 2022-10-02 13:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("univ_app", "0018_rename_given_answer_givenanswer"),
    ]

    operations = [
        migrations.CreateModel(
            name="TakenTest",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("score", models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name="AnsweredQuestion",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("correct", models.BooleanField(default=False)),
                (
                    "related_question",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="univ_app.question",
                    ),
                ),
                (
                    "related_taken_test",
                    models.ForeignKey(
                        null=True,
                        on_delete=django.db.models.deletion.CASCADE,
                        to="univ_app.takentest",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="givenanswer",
            name="related_answered_question",
            field=models.ForeignKey(
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="univ_app.answeredquestion",
            ),
        ),
    ]
