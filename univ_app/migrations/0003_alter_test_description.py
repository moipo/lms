# Generated by Django 4.0.5 on 2022-08-15 13:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('univ_app', '0002_question_answered_correctly_test_score'),
    ]

    operations = [
        migrations.AlterField(
            model_name='test',
            name='description',
            field=models.TextField(blank=True),
        ),
    ]
