# Generated by Django 4.1.3 on 2023-01-28 06:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('univ_app', '0029_alter_answeredcommontask_file'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answeredcommontask',
            name='grade',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='takentest',
            name='grade',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.DeleteModel(
            name='Grade',
        ),
    ]
