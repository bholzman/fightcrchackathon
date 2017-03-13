from django.contrib import admin
from django.contrib.postgres.fields import ArrayField
from django.forms import Textarea


# Register your models here.
from .models import UserText, FAQ, CRCTrial

admin.site.register(UserText)
admin.site.register(FAQ)

@admin.register(CRCTrial)
class CRCTrialAdmin(admin.ModelAdmin):
    list_display = ('brief_title', 'nct_id', 'reviewed', 'updated_date', 'date_trial_added')
    list_display_links = ('brief_title', 'nct_id')

    fieldsets = (
        (None, {'fields': (('nct_id','trial_link'),'brief_title','reviewed')}),
        ('For Review', {'fields': (
            'is_crc_trial', 'is_immunotherapy_trial',
            'category', 'prior_io_ok',
            'comments', 'resources', 'urls')}),
        ('Additional Information', {'fields': (
            'title', 'program_status', 'locations',
            'date_trial_added', 'updated_date',
            'phase', 'intervention_types', 'drug_names',
            'description', 'min_age', 'max_age', 'gender',
            'inclusion_criteria', 'exclusion_criteria',
            'contact_phones', 'contact_emails')}))

    formfield_overrides = {
        ArrayField: {'widget': Textarea(attrs={'rows':4})}
    }

    search_fields = ['nct_id', 'brief_title']
