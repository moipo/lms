# Generated by Django 4.1.1 on 2022-10-02 13:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('univ_app', '0019_takentest_answeredquestion_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='takentest',
            name='related_test',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='univ_app.test'),
        ),
    ]
