# Generated by Django 4.2.6 on 2023-10-30 19:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CertTracApp', '0018_rename_topic_course_subject'),
    ]

    operations = [
        migrations.RenameField(
            model_name='takes',
            old_name='sub_topic',
            new_name='course',
        ),
    ]
