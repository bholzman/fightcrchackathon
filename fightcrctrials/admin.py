from django.contrib import admin
from django.contrib.admin.views.main import ChangeList
from django.contrib.postgres.fields import ArrayField
from django.forms import Textarea


# Register your models here.
from .models import UserText, FAQ, CRCTrial, MobileFAQ2

admin.site.register(UserText)

class Phase1ChangeList(ChangeList):
    def get_queryset(self, request):
        qs = super(Phase1ChangeList, self).get_queryset(request)
        return qs.filter(screened__isnull=True).exclude(reviewed=False)

class Phase2ChangeList(ChangeList):
    def get_queryset(self, request):
        qs = super(Phase2ChangeList, self).get_queryset(request)
        return qs.exclude(reviewed=False)


@admin.register(CRCTrial)
class CRCTrialAdmin(admin.ModelAdmin):
    save_on_top = True

    def get_changelist(self, request):
        if request.user.has_perm('fightcrctrials.phase_1') and not request.user.is_superuser:
            return Phase1ChangeList
        elif request.user.has_perm('fightcrctrials.phase_2') and not request.user.is_superuser:
            return Phase2ChangeList
        else:
            return ChangeList

    def get_list_display(self, request):
        if request.user.has_perm('fightcrctrials.phase_1') and not request.user.is_superuser:
            return ('brief_title', 'nct_id', 'screened', 'updated_date', 'date_trial_added')
        elif request.user.has_perm('fightcrctrials.phase_2') and not request.user.is_superuser:
            return ('brief_title', 'nct_id', 'screened', 'reviewed', 'updated_date', 'date_trial_added')
        else:
            return ('brief_title', 'nct_id', 'screened', 'reviewed', 'additional_review', 'updated_date', 'date_trial_added')

    def get_list_display_links(self, request, list_display):
        return ('brief_title', 'nct_id')

    def get_fieldsets(self, request, obj=None):
        if request.user.has_perm('fightcrctrials.phase_1') and not request.user.is_superuser:
            top_fields = (('nct_id','trial_link'),('brief_title','conditions'),'screened','review_comments')
        else:
            top_fields = (('nct_id','trial_link'),('brief_title','conditions'),'screened','reviewed',('additional_review','review_comments'))

        return (
            (None, {'fields': top_fields}),
            ('For Review', {'fields': (
                'is_crc_trial', 'is_immunotherapy_trial',
                'category', 'prior_io_ok',
                'comments', 'resources', 'keywords', 'drug_brand_names')}),
            ('Additional Information', {'fields': (
                'title', 'drug_names', 'program_status', 'locations',
                'urls', 'date_trial_added', 'updated_date', 'phase', 'intervention_types',
                'description', 'min_age', 'max_age', 'gender',
                'inclusion_criteria', 'exclusion_criteria',
                'contact_phones', 'contact_emails')}))

    formfield_overrides = {
        ArrayField: {'widget': Textarea(attrs={'rows':4})}
    }

    search_fields = ['nct_id', 'brief_title']

    def get_readonly_fields(self, request, obj=None):
        if request.user.is_superuser:
            return ()
        return (
            'title', 'program_status', 'locations', 'urls', 'date_trial_added', 'updated_date', 'phase',
            'intervention_types', 'drug_names', 'description', 'min_age', 'max_age', 'gender', 'inclusion_criteria',
            'exclusion_criteria', 'contact_phones', 'contact_emails')

@admin.register(FAQ)
class FAQAdmin(admin.ModelAdmin):
    ordering = ('id',)

@admin.register(MobileFAQ2)
class MobileFAQAdmin(admin.ModelAdmin):
    ordering = ('id',)
