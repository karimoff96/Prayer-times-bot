# Generated by Django 4.0.2 on 2023-01-25 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('prayertime', '0002_rename_users_user_alter_user_options_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Send',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField()),
                ('current', models.IntegerField()),
                ('total', models.IntegerField()),
                ('msg_id', models.BigIntegerField()),
            ],
        ),
    ]
