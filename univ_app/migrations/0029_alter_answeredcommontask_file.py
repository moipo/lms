# Generated by Django 4.1.3 on 2023-01-11 18:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('univ_app', '0028_answeredcommontask_common_task'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answeredcommontask',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='uploads/answered_common_tasks/'),
        ),
    ]