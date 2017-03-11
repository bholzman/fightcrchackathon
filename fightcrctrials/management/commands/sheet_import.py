from datetime import date
from django.core.management.base import BaseCommand
import json

from fightcrctrials.models import CRCTrial, CRCTrials

class Command(BaseCommand):
    help = 'Import clinical trials from google sheet'

    def handle(self, *args, **kwargs):
        trials = json.loads(CRCTrials().get_trials_data())
        for data in trials['data']:
            if data[2].startswith('NCT'):
                trial = CRCTrial.objects.create(
                    date_trial_added=date.today(),
                    updated_date=date.today(),
                    category=data[0],
                    drug_names=[data[1]],
                    nct_id=data[2],
                    is_crc_trial='Tw' in data[3],
                    is_immunotherapy_trial='Im' in data[3],
                    locations=data[4],
                    comments=data[5],
                    prior_io_ok=(data[6] == 'Yes'),
                    resources=data[7],
                    reviewed=True)
