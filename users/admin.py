from django.contrib import admin
from .models import Motorcycle, Client, User
from django.contrib.auth.models import Group

# Register your models here.

admin.site.register(User)
admin.site.register(Motorcycle)
admin.site.register(Client)
admin.site.unregister(Group)


