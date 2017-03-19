"""
Updates our existing CRT trials with any new
information sourced from the aact datatbase.
"""
from __future__ import print_function
from django.utils import timezone

from fightcrctrials.aact import AACT
from fightcrctrials.email import send_email
from fightcrctrials.models import CRCTrial, ScriptRuns
from fightcrctrials.scripts.trial_importer import update_or_create

SCRIPT = 'update_existing_trials'


class CRCTrialsUpdater(object):
    def __init__(self, cutoff_days):
        self.cutoff_days = cutoff_days
        self.script_run = ScriptRuns.objects.create(script=SCRIPT)
        self.aact = AACT()

    def update_existing_trials(self):
        record_count = 0
        errors = []
        try:
            # query trials that we have
            existing_ids = [k['nct_id'] for k in CRCTrial.objects.all().values('nct_id')]

            trial_query = self.aact.trial_query()
            trial_query = self.aact.add_newly_updated_condition(trial_query, self.cutoff_days)
            for nct_id in existing_ids:
                result = self.aact.engine.execute(trial_query, nct_id=nct_id)
                record = result.first()
                if record:
                    record_count = record_count + 1
                    try:
                        update_or_create(record)
                    except Exception as e:
                        error_message = "Could not update {}: {}".format(nct_id, e)
                        errors.append(error_message)
                        print(error_message)
            self.script_run.success = True
        except Exception as e:
            print("{} failed: {}".format(SCRIPT, e))
        finally:
            self.script_run.finish_time = timezone.now()
            self.script_run.record_count = record_count
            self.script_run.save()
        if errors:
            send_email("Errors from {}".format(SCRIPT), "\n".join(errors))


def run(cutoff_days=None):
    """
    cutoff_days: the number of days prior to today that we query for updates/change
    """
    start_time = timezone.now()
    print("Script {} starting at {}".format(SCRIPT, start_time))
    if cutoff_days is None:
        # set to 1+days since last successful run, or to 2 if there is no such run
        last_successful_run = ScriptRuns.objects.filter(script=SCRIPT, success=True).order_by('-finish_time').first()
        if last_successful_run:
            print("Last successful run found at {}".format(last_successful_run.finish_time))
            cutoff_days = (start_time - last_successful_run.finish_time).days + 1
        else:
            print("No last successful run found")
            cutoff_days = 2
    print("Cutoff days: {}".format(cutoff_days))
    CRCTrialsUpdater(int(cutoff_days)).update_existing_trials()
