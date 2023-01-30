from django.contrib import admin
from .models import User, Media, Send, Time

# Register your models here.
admin.site.register(User)
admin.site.register(Media)
admin.site.register(Send)
admin.site.register(Time)
