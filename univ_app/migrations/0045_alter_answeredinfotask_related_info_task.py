# Generated by Django 4.1.3 on 2023-02-03 18:41

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('univ_app', '0044_alter_answeredcommontask_common_task'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answeredinfotask',
            name='related_info_task',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='univ_app.infotask'),
        ),
    ]