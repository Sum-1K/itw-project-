# Generated by Django 5.1.2 on 2024-11-01 18:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0007_completedlesson_lesson_completed_by'),
    ]

    operations = [
        migrations.AlterField(
            model_name='quiz',
            name='quiz_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]
