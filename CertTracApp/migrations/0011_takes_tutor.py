# Generated by Django 4.2.6 on 2023-10-27 01:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CertTracApp', '0010_remove_takes_tutor_alter_takes_course'),
    ]

    operations = [
        migrations.AddField(
            model_name='takes',
            name='tutor',
            field=models.IntegerField(default=0),
        ),
    ]
