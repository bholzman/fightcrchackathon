from django.contrib import admin

# Register your models here.
from .models import UserText, FAQ, CRCTrial

admin.site.register(UserText)
admin.site.register(FAQ)

@admin.register(CRCTrial)
class CRCTrialAdmin(admin.ModelAdmin):
    list_display = ('title', 'nct_id', 'reviewed', 'updated_date', 'date_trial_added')
    list_display_links = ('title', 'nct_id')
