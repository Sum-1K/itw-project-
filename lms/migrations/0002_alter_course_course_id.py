# Generated by Django 5.1.2 on 2024-10-25 21:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('lms', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='course',
            name='course_id',
            field=models.AutoField(primary_key=True, serialize=False),
        ),
    ]