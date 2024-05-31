from django.contrib import admin
from yuecheapp.models import User, Vehicle
from django.contrib.auth.admin import UserAdmin

admin.site.register(User, UserAdmin)
admin.site.register(Vehicle)