# Generated by Django 4.0.2 on 2023-01-31 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Media',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(blank=True, max_length=200, null=True)),
                ('media', models.FileField(blank=True, null=True, upload_to='')),
                ('active', models.BooleanField(default=True)),
                ('cr_on', models.DateTimeField(auto_now_add=True)),
            ],
        ),
        migrations.CreateModel(
            name='Send',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('count', models.IntegerField()),
                ('current', models.IntegerField()),
                ('msg_id', models.BigIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Time',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('city_id', models.IntegerField(default=0)),
                ('city', models.CharField(blank=True, max_length=256, null=True)),
                ('updated_date', models.DateField(blank=True, null=True)),
                ('updated_time', models.TimeField(blank=True, null=True)),
                ('date', models.DateField(auto_now_add=True)),
                ('kun', models.CharField(blank=True, max_length=128, null=True)),
                ('tong', models.TimeField(blank=True, null=True)),
                ('quyosh', models.TimeField(blank=True, null=True)),
                ('peshin', models.TimeField(blank=True, null=True)),
                ('asr', models.TimeField(blank=True, null=True)),
                ('shom', models.TimeField(blank=True, null=True)),
                ('xufton', models.TimeField(blank=True, null=True)),
            ],
            options={
                'verbose_name': 'Time',
                'verbose_name_plural': 'Times',
            },
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_id', models.BigIntegerField(default=0, unique=True)),
                ('username', models.CharField(blank=True, max_length=30, null=True)),
                ('first_name', models.CharField(blank=True, max_length=30, null=True)),
                ('last_name', models.CharField(blank=True, max_length=30, null=True)),
                ('phone_number', models.CharField(blank=True, max_length=128, null=True)),
                ('address', models.CharField(blank=True, max_length=200, null=True)),
                ('active', models.BooleanField(default=False)),
                ('language', models.CharField(blank=True, max_length=100, null=True)),
                ('cr_on', models.DateTimeField(auto_now_add=True)),
                ('step', models.IntegerField(default=0)),
            ],
            options={
                'verbose_name': 'User',
                'verbose_name_plural': 'Users',
            },
        ),
        migrations.AddIndex(
            model_name='user',
            index=models.Index(fields=['username'], name='prayertime__usernam_1e0b45_idx'),
        ),
        migrations.AddIndex(
            model_name='time',
            index=models.Index(fields=['city'], name='prayertime__city_49b1c4_idx'),
        ),
    ]
