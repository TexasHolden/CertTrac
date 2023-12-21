# Generated by Django 4.2.6 on 2023-10-30 19:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CertTracApp', '0015_rename_course_subtopic_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='InPersonTrainingSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_topic', models.CharField(max_length=40)),
                ('date', models.CharField(max_length=40)),
                ('training_time', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
        migrations.CreateModel(
            name='TotalTrainingSession',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sub_topic', models.CharField(max_length=40)),
                ('date', models.CharField(max_length=40)),
                ('training_time', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
    ]
