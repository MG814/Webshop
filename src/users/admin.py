from django.contrib import admin

from .models import Profile, Address, User

admin.site.register(Profile)
admin.site.register(Address)
admin.site.register(User)
