"""
Checks that the update_existing_trials and download_new_trials scripts have
run successfully recently, and have updated/created new trials.
"""
from __future__ import print_function
from django.utils import timezone
import os

from fightcrctrials.email import send_email
from fightcrctrials.models import ScriptRuns, CRCTrial
from fightcrctrials.scripts import update_existing_trials, download_new_trials


SCRIPT = 'check_script_runs'


def _alert(message):
    print(message)
    send_email("Alert from {}".format(SCRIPT), message)


def _alert_no_recent_run(script, last_finish_time):
    _alert('Script {} has not had a successful run since {}'.format(script, last_finish_time))


def _alert_no_recent_records(script, first_finish_time):
    _alert('Script {} has not found any records to process since {}'.format(script, first_finish_time))


def _alert_too_many_unreviewed(unreviewed_count):
    _alert('There are {} unreviewed trials'.format(unreviewed_count))


def run():
    start_time = timezone.now()
    print("Script {} starting at {}".format(SCRIPT, start_time))

    days_since_run = os.environ.get('ALERT_THRESHOLD_DAYS_SINCE_RUN')
    runs_since_data = os.environ.get('ALERT_THRESHOLD_RUNS_SINCE_DATA')
    unreviewed = os.environ.get('ALERT_THRESHOLD_UNREVIEWED')

    # get the last successful run for each script and check that it wasn't too long ago
    for script in update_existing_trials, download_new_trials:
        last_successful_run = ScriptRuns.objects.filter(
            script=script.SCRIPT, success=True).order_by('-finish_time').first()
        if last_successful_run:
            if (start_time - last_successful_run.finish_time).days > days_since_run:
                _alert_no_recent_run(script.SCRIPT, last_successful_run.finish_time)

            # sum the record count for the last runs_since_data successful runs and ensure it is >= 1
            last_n_successful_runs = ScriptRuns.objects.filter(
                script=script.SCRIPT, success=True).order_by('-finish_time')[:runs_since_data]
            record_count = sum(run.record_count for run in last_n_successful_runs)
            if record_count == 0:
                _alert_no_recent_records(script.SCRIPT, [r for r in last_n_successful_runs][-1].finish_time)
        else:
            # if there are no successful runs at all, this is probably the very first time this
            # script has run, so just ignore it
            pass

    # check that there aren't too many unreviewed trials
    unreviewed_count = CRCTrial.objects.filter(reviewed=False).count()
    if unreviewed_count > unreviewed:
        _alert_too_many_unreviewed(unreviewed_count)
