# Generated by Django 3.2.4 on 2023-01-05 13:23

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('univ_app', '0025_alter_commontask_file'),
    ]

    operations = [
        migrations.CreateModel(
            name='InfoTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(blank=True, default='', max_length=200)),
                ('description', models.TextField(blank=True, default='')),
                ('created_at', models.DateTimeField(auto_now_add=True, null=True)),
                ('file', models.FileField(blank=True, null=True, upload_to='uploads/info_tasks/')),
                ('created_by', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='univ_app.teacher')),
                ('subject', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='univ_app.subject')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AnsweredInfoTask',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('finished_at', models.DateTimeField(blank=True, null=True)),
                ('was_checked', models.BooleanField(blank=True, null=True)),
                ('student', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, to='univ_app.student')),
            ],
            options={
                'abstract': False,
            },
        ),
    ]