# Generated by Django 5.1.2 on 2024-10-29 16:01

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0006_remove_certificate_id_certificate_certificate_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='CompletedLesson',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('completion_date', models.DateTimeField(auto_now_add=True)),
                ('lesson', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='lms.lesson')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'unique_together': {('user', 'lesson')},
            },
        ),
        migrations.AddField(
            model_name='lesson',
            name='completed_by',
            field=models.ManyToManyField(related_name='completed_lessons', through='lms.CompletedLesson', to=settings.AUTH_USER_MODEL),
        ),
    ]
