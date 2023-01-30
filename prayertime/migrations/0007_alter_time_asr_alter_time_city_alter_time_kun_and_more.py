# Generated by Django 4.0.2 on 2023-01-28 16:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prayertime', '0006_time_created_time_time_update_time_alter_time_date'),
    ]

    operations = [
        migrations.AlterField(
            model_name='time',
            name='asr',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='time',
            name='city',
            field=models.CharField(blank=True, max_length=256, null=True),
        ),
        migrations.AlterField(
            model_name='time',
            name='kun',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='time',
            name='pewn',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='time',
            name='quyosh',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='time',
            name='shom',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='time',
            name='tong',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='time',
            name='update_time',
            field=models.TimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='time',
            name='xufton',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
