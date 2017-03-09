from apiclient.discovery import build
from django.db import models
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


# this data model will read from the CRC Trials google sheet
class CRCTrials(object):
    def __init__(self):
        self.trials = self.get_trials_data()

    def get_trials_data(self):
        # read from cache with 30 minute expiration
        cache_file = '.trials'
        if os.path.exists(cache_file):
            with open(cache_file, 'r') as fh:
                data = json.load(fh)
                if data['created_at'] < time.time() + 30 * 60:
                    return data['trials']

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
        data = {'created_at': time.time(), 'trials': self._transform(response['values'])}
        # use a temp file so we can atomically rename it
        temp_file = '{}.{}'.format(cache_file, random.random())
        with open(temp_file, 'w') as fh:
            json.dump(data, fh)
        os.rename(temp_file, cache_file)
        return data['trials']

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

        trials = []
        cur_category = None
        for row in values[1:]:
            if len(row) == 1:  # header row
                cur_category = row[0]
                trials.append({'header': cur_category})
            else:
                drug = row[0]
                trial_type = row[1]
                locations = row[2].split(',')
                nct = row[3]
                comments = row[5]
                prior_io_ok = 0
                publications = []
                if len(row) > 6 and row[6]:
                    prior_io_ok = 1
                if len(row) > 7:
                    publications = row[7:]
                trials.append({
                    'category': cur_category,
                    'drug': drug,
                    'nct': nct,
                    'type': trial_type,
                    'locations': locations,
                    'comments': comments,
                    'prior_io_ok': prior_io_ok,
                    'publications': publications
                })

        return trials
