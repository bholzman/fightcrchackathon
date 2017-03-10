from apiclient.discovery import build
from django.db import models
from django.contrib.postgres.fields import ArrayField
from httplib2 import Http
import fcntl
import json
from oauth2client.service_account import ServiceAccountCredentials
import os
import random
import time

# Create your models here.
class Greeting(models.Model):
    when = models.DateTimeField('date created', auto_now_add=True)


class UserText(models.Model):
    tag = models.SlugField(unique=True)
    text = models.TextField()
    def __str__(self):
        return self.tag


class FAQ(models.Model):
    question = models.TextField(unique=True)
    answer = models.TextField()
    def __str__(self):
        return self.question


# this data model will read from the CRC Trials google sheet
class CRCTrial(models.Model):
    category = models.CharField(max_length=100)
    nct_id = models.CharField(unique=True, max_length=100)
    updated_date = models.DateField()
    date_trial_added = models.DateField()
    brief_title = models.CharField(max_length=300, blank=True)
    title = models.CharField(max_length=300)
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
        ("Terminated", "Terminated")))
    phase = models.CharField(max_length=20, choices=(
        ("Phase 1", "Phase 1"),
        ("Early Phase 1", "Early Phase 1"),
        ("Phase 4", "Phase 4"),
        ("Phase 1/Phase 2", "Phase 1/Phase 2"),
        ("Phase 2/Phase 3", "Phase 2/Phase 3"),
        ("Phase 2", "Phase 2"),
        ("Phase 3", "Phase 3")), blank=True)
    min_age = models.IntegerField(null=True)
    max_age = models.IntegerField(null=True)
    gender = models.CharField(max_length=1, choices=(('M', 'Male'), ('F', 'Female')), blank=True)
    inclusion_criteria = models.TextField(null=True)
    exclusion_criteria = models.TextField(null=True)
    locations = ArrayField(models.CharField(max_length=100))
    contact_phones = ArrayField(models.CharField(max_length=100), null=True)
    contact_emails = ArrayField(models.EmailField(), null=True)
    urls = ArrayField(models.URLField(max_length=200), null=True)
    prior_io_ok = models.BooleanField(default=False)
    description = models.TextField(null=True)
    is_crc_trial = models.BooleanField(default=False)
    is_immunotherapy_trial = models.BooleanField(default=False)
    comments = models.TextField(blank=True)
    resources = ArrayField(models.URLField(max_length=200), null=True)
    drug_names = ArrayField(models.CharField(max_length=300))
    intervention_types = ArrayField(models.CharField(max_length=200), null=True)
    reviewed = models.BooleanField(default=False)

    def __str__(self):
        return '{} ({})'.format(self.brief_title, self.nct_id)

    @classmethod
    def trials_json(cls):
        reviewed = CRCTrial.objects.filter(reviewed=True)
        trial_data = []
        for trial in reviewed:
            trial_type = ''
            if trial.is_crc_trial and trial.is_immunotherapy_trial:
                trial_type = 'Im OR Tw'
            elif trial.is_crc_trial:
                trial_type = 'Tw'
            elif trial.is_immunotherapy_trial:
                trial_type = 'Im'

            trial_data.append([
                trial.category,
                ', '.join(trial.drug_names),
                trial.nct_id,
                trial_type,
                trial.locations,
                trial.comments,
                trial.prior_io_ok,
                trial.resources])

        return json.dumps({
            'header': ['Subtype', 'Drug', 'NCT', 'Type', 'Locations',
                       'Comments', 'Prior Immunotherapy OK', 'Publications'],
            'data': trial_data
        })


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
                if len(row) > 6 and row[6]:
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

        return {
            'header': self._header,
            'data': data
        }
