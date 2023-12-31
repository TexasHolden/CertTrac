# Generated by Django 4.2.6 on 2023-10-27 01:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('CertTracApp', '0012_alter_takes_tutor'),
    ]

    operations = [
        migrations.AddField(
            model_name='takes',
            name='semester',
            field=models.CharField(default='', max_length=40),
        ),
        migrations.AlterField(
            model_name='course',
            name='subject',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='inpersontrainingsession',
            name='date',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='totaltrainingsession',
            name='date',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='tutor',
            name='date_hired',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='tutor',
            name='first_name',
            field=models.CharField(max_length=40),
        ),
        migrations.AlterField(
            model_name='tutor',
            name='last_name',
            field=models.CharField(max_length=40),
        ),
    ]
