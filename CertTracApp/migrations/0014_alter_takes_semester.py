# Generated by Django 4.2.6 on 2023-10-27 01:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CertTracApp', '0013_takes_semester_alter_course_subject_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='takes',
            name='semester',
            field=models.CharField(max_length=40),
        ),
    ]