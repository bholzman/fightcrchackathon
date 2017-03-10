from django.contrib import admin

# Register your models here.
from .models import UserText, FAQ

admin.site.register(UserText)
admin.site.register(FAQ)
