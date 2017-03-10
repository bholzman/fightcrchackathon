from django.contrib import admin

# Register your models here.
from .models import UserText, FAQ, CRCTrial

admin.site.register(UserText)
admin.site.register(FAQ)
admin.site.register(CRCTrial)
