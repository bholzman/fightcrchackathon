from googleapiclient.discovery import build
from django.db import models
from django.contrib.postgres.fields import ArrayField
from django.utils import timezone
from httplib2 import Http
import fcntl
import json
from oauth2client.service_account import ServiceAccountCredentials
import os
import random
import time

# Create your models here.
class UserText(models.Model):
    tag = models.SlugField(unique=True)
    text = models.TextField()
    def __str__(self):
        return self.tag


class FAQ(models.Model):
    class Meta:
        verbose_name = 'FAQ'
        verbose_name_plural = 'FAQs'

    question = models.TextField(unique=True)
    answer = models.TextField()
    def __str__(self):
        return self.question

    @classmethod
    def faq_json(cls):
        faqs = cls.objects.order_by('id').all()
        raw_data = [{
            'question': faq.question,
            'answer': faq.answer
        } for faq in faqs]
        return json.dumps(raw_data)

class MobileFAQ(FAQ):
    pass

class MobileFAQ2(models.Model):
    class Meta:
        verbose_name = 'Mobile FAQ'
        verbose_name_plural = 'Mobile FAQs'

    question = models.TextField(unique=True)
    answer = models.TextField()
    def __str__(self):
        return self.question

    @classmethod
    def faq_json(cls):
        faqs = cls.objects.order_by('id').all()
        raw_data = [{
            'question': faq.question,
            'answer': faq.answer
        } for faq in faqs]
        return json.dumps(raw_data)

class DeletedCRCTrial(models.Model):
    deleted_at = models.DateField(auto_now_add=True)
    nct_id = models.CharField(unique=True, max_length=100)


class CRCTrial(models.Model):
    class Meta:
        permissions = (("phase_1", "Phase 1 reviewer"), ("phase_2", "Phase 2 reviewer"),)
        verbose_name = 'CRC Trial'
        verbose_name_plural = 'CRC Trials'

    nct_id = models.CharField("NCT ID", unique=True, max_length=100)
    trial_link = models.URLField(max_length=200, null=True, blank=True,
        help_text="Optional, defaults to the page at clinicaltrials.gov for this NCT ID")
    brief_title = models.CharField(max_length=300, null=True, blank=True)
    screened = models.NullBooleanField(default=None, null=True, blank=True)
    screened.verbose_name = 'Triaged'
    reviewed = models.NullBooleanField(default=None, null=True, blank=True)
    reviewed.verbose_name = 'Approved'
    action_required = models.CharField(default=None, null=True, blank=True, choices=(('L1: Read', 'L1: Read'), ('L2: Read', 'L2 Read'), ('L2: Update COMM', 'L2: Update COMM'), ('L2: Update LINKS', 'L2: Update LINKS'), ('MAB: Review', 'MAB: Review'), ('Unknown', 'Unknown')), max_length=100)
    action_required.verbose_name = 'Action Required'
    review_comments = models.TextField(null=True, blank=True)
    is_crc_trial = models.BooleanField('CRC-directed trial', default=False, blank=True)
    is_immunotherapy_trial = models.BooleanField('Immunotherapy trial', default=False, blank=True)
    category = models.CharField('Trial sub-type', max_length=100, null=True, blank=True)
    prior_io_ok = models.BooleanField(default=False, blank=True)
    comments = models.TextField(null=True, blank=True)
    resources = ArrayField(models.URLField(max_length=250), null=True, blank=True)
    resources.verbose_name = 'Helpful Links'
    keywords = ArrayField(models.CharField(max_length=100), null=True, blank=True)
    drug_brand_names = ArrayField(models.CharField(max_length=300), null=True, blank=True)
    title = models.CharField(max_length=500, null=True, blank=True)
    conditions = ArrayField(models.CharField(max_length=300), null=True, blank=True)
    program_status = models.CharField(max_length=30, choices=(
        ("Temporarily not available", "Temporarily not available"),
        ("Active, not recruiting", "Active, not recruiting"),
        ("Suspended", "Suspended"),
        ("Recruiting", "Recruiting"),
        ("Withheld", "Withheld"),
        ("Enrolling by invitation", "Enrolling by invitation"),
        ("Completed", "Completed"),
        ("No longer available", "No longer available"),
        ("Unknown status", "Unknown status"),
        ("Withdrawn", "Withdrawn"),
        ("Available", "Available"),
        ("Approved for marketing", "Approved for marketing"),
        ("Not yet recruiting", "Not yet recruiting"),
        ("Terminated", "Terminated")), null=True, blank=True)
    locations = ArrayField(models.CharField(max_length=100), null=True, blank=True)
    urls = ArrayField(models.URLField(max_length=200), null=True, blank=True)
    date_trial_added = models.DateField(null=True, blank=True)
    updated_date = models.DateField(null=True, blank=True)
    phase = models.CharField(max_length=20, choices=(
        ("N/A", "N/A"),
        ("Phase 1", "Phase 1"),
        ("Early Phase 1", "Early Phase 1"),
        ("Phase 4", "Phase 4"),
        ("Phase 1/Phase 2", "Phase 1/Phase 2"),
        ("Phase 2/Phase 3", "Phase 2/Phase 3"),
        ("Phase 2", "Phase 2"),
        ("Phase 3", "Phase 3")), null=True, blank=True)
    intervention_types = ArrayField(models.CharField(max_length=200), null=True, blank=True)
    drug_names = ArrayField(models.CharField(max_length=300), null=True, blank=True)
    description = models.TextField(null=True, blank=True)
    min_age = models.IntegerField(null=True, blank=True)
    max_age = models.IntegerField(null=True, blank=True)
    gender = models.CharField(max_length=1, choices=(('M', 'Male'), ('F', 'Female'), ('A', 'All')), null=True, blank=True)
    inclusion_criteria = models.TextField(null=True, blank=True)
    exclusion_criteria = models.TextField(null=True, blank=True)
    contact_phones = ArrayField(models.CharField(max_length=100), null=True, blank=True)
    contact_emails = ArrayField(models.EmailField(), null=True, blank=True)

    def __str__(self):
        return '%s (%s)' % (self.brief_title, self.nct_id)

    def __unicode__(self):
        return u'%s (%s)' % (self.brief_title, self.nct_id)

    @classmethod
    def trials_json(cls):
        reviewed = CRCTrial.objects.filter(reviewed=True)
        # TODO
        # would be nice to use django's built-in serializer, but it does
        # not handle the ArrayFields correctly. Should extend the serializer
        # instead, but for now we'll just do something dumb.
        raw_data = [
            {'nct_id': r.nct_id,
             'trial_link': r.trial_link,
             'brief_title': r.brief_title,
             'date_trial_added': str(r.date_trial_added),
             'updated_date': str(r.updated_date),
             'is_crc_trial': r.is_crc_trial,
             'is_immunotherapy_trial': r.is_immunotherapy_trial,
             'intervention_types': r.intervention_types,
             'drug_names': r.drug_names,
             'drug_brand_names': r.drug_brand_names,
             'subtype': r.category,
             'conditions': r.conditions,
             'title': r.title,
             'program_status': r.program_status,
             'phase': r.phase,
             'min_age': r.min_age,
             'max_age': r.max_age,
             'gender': r.gender,
             'inclusion_criteria': r.inclusion_criteria,
             'exclusion_criteria': r.exclusion_criteria,
             'locations': r.locations,
             'contact_phones': r.contact_phones,
             'contact_emails': r.contact_emails,
             'urls': r.urls,
             'prior_io_ok': r.prior_io_ok,
             'description': r.description,
             'comments': r.comments,
             'keywords': r.keywords,
             'publications': r.resources} for r in reviewed]
        return json.dumps(raw_data)


class ScriptRuns(models.Model):
    script = models.CharField(max_length=200)
    start_time = models.DateTimeField(default=timezone.now)
    finish_time = models.DateTimeField(db_index=True, null=True, blank=True)
    success = models.BooleanField(default=False)
    record_count = models.IntegerField(null=True, blank=True)


# this data model will read from the CRC Trials google sheet
class CRCTrials(object):
    _header = ['Subtype', 'Drug', 'NCT', 'Type', 'Locations', 'Comments', 'Prior Immunotherapy OK', 'Publications']

    def __init__(self, caching_enabled=True):
        self._caching_enabled = caching_enabled
        self.trials = self.get_trials_data()

    def _get_spreadsheet_data(self):
        # read from cache with 30 minute expiration
        cache_file = '.crchacks'
        if self._caching_enabled and os.path.exists(cache_file):
            with open(cache_file, 'r') as fh:
                data = json.load(fh)
                if data['created_at'] < time.time() + 30 * 60:
                    return data['response']

        # if we got here, there is no cache or it has expired
        scopes = [
            'https://www.googleapis.com/auth/drive',
            'https://www.googleapis.com/auth/drive.readonly',
            'https://www.googleapis.com/auth/spreadsheets',
            'https://www.googleapis.com/auth/spreadsheets.readonly'
        ]
        root, _ = os.path.split(__file__)
        keyfile = os.path.join(root, '..', 'etc', 'Google-Service-Account.json')
        credentials = ServiceAccountCredentials.from_json_keyfile_name(
            keyfile, scopes=scopes)

        http = credentials.authorize(Http())

        self._api = build('sheets', 'v4', http=http)

        spreadsheetId = '1HV-WiZTiJORIOTQhsgAC19Oe5bOuSMCVBDJ8woBFdnQ'
        response = self._api.spreadsheets().values().get(spreadsheetId=spreadsheetId, range='A2:J999').execute()
        data = {'created_at': time.time(), 'response': response}
        # use a temp file so we can atomically rename it
        temp_file = '{}.{}'.format(cache_file, random.random())
        with open(temp_file, 'w') as fh:
            json.dump(data, fh)
        os.rename(temp_file, cache_file)

        return data['response']

    def get_trials_data(self):
        response = self._get_spreadsheet_data()

        return self._transform(response['values'])

    def _transform(self, values):
        # transform raw data from spreadsheet into this format:
        # [
        #   {'header': CATEGORY},
        #   {'category': CATEGORY,
        #    'drug': DRUG,
        #    'nct': NCT,
        #    'type': IM/TW,
        #    'locations': [...],
        #    'comments': [...],
        #    'prior_io_ok': 1/0,
        #    'publications': [...]},
        #   ...other trials in this category...
        #   {'header': CATEGORY2},
        #   ...
        #   ]
        # sanity check that the column headers are as expected
        assert(values[0] == [
            'Drug', '"Im"/"Tw"', 'Locations (as of 02/2017)', 'NCT#', 'NCT# Link', 'Comments',
            'Allow prior PD-1? ', 'Publication?', 'Publication #2?'])

        data = []

        cur_category = None
        for row in values[1:]:
            if len(row) == 1:  # header row
                cur_category = row[0]
                # trials.append({'header': cur_category})
            else:
                drug = row[0]
                trial_type = row[1]
                locations = [x.strip() for x in row[2].split(',') if x]
                nct = row[3]
                comments = row[5]
                prior_io_ok = "No"
                publications = []
                if len(row) > 6 and row[6].startswith('PD1-OK'):
                    prior_io_ok = "Yes"
                if len(row) > 7:
                    publications = row[7:]
                data.append([
                    cur_category,
                    drug,
                    nct,
                    trial_type,
                    locations,
                     comments,
                    prior_io_ok,
                    publications
                ])

        return json.dumps({
            'header': self._header,
            'data': data
        })

import signals
