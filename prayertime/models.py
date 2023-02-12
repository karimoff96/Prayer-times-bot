from django.db import models


# Create your models here.
class User(models.Model):
    user_id = models.BigIntegerField(default=0, unique=True)
    username = models.CharField(max_length=30, blank=True, null=True)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    phone_number = models.CharField(max_length=128, blank=True, null=True)
    city = models.CharField(max_length=200, blank=True, null=True)
    active = models.BooleanField(default=False)
    language = models.CharField(max_length=100, blank=True, null=True)
    cr_on = models.DateTimeField(auto_now_add=True)
    step = models.IntegerField(default=0)

    def __str__(self):
        return self.first_name

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'
        indexes = [
            models.Index(fields=['username'])
        ]


class Media(models.Model):
    name = models.CharField(max_length=200, blank=True, null=True)
    media = models.FileField(blank=True, null=True)
    active = models.BooleanField(default=True)
    cr_on = models.DateTimeField(auto_now_add=True)


class Send(models.Model):
    count = models.IntegerField()
    current = models.IntegerField()
    msg_id = models.BigIntegerField()


class Time(models.Model):
    city_id = models.IntegerField(default=0)
    city = models.CharField(max_length=256, blank=True, null=True)
    updated_date = models.DateField(blank=True, null=True)
    updated_time = models.TimeField(blank=True, null=True)
    date = models.DateField(auto_now_add=True, blank=True)
    kun = models.CharField(max_length=128, blank=True, null=True)
    tong = models.TimeField(blank=True, null=True)
    quyosh = models.TimeField(blank=True, null=True)
    peshin = models.TimeField(blank=True, null=True)
    asr = models.TimeField(blank=True, null=True)
    shom = models.TimeField(blank=True, null=True)
    xufton = models.TimeField(blank=True, null=True)

    class Meta:
        verbose_name = 'Time'
        verbose_name_plural = 'Times'
        indexes = [
            models.Index(fields=['city'])
        ]

    def __str__(self):
        return self.city
