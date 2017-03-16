"""
Checks that the update_existing_trials and download_new_trials scripts have
run successfully recently, and have updated/created new trials.
"""
from __future__ import print_function
from django.utils import timezone
import os
import sendgrid
from sendgrid.helpers.mail import Email, Content, Mail

from fightcrctrials.email import send_email
from fightcrctrials.models import ScriptRuns
from fightcrctrials.scripts import update_existing_trials, download_new_trials


SCRIPT = 'check_script_runs'


def _alert(message):
    print(message)
    send_email("Alert from {}".format(SCRIPT), message)


def _alert_no_recent_run(script, last_finish_time):
    _alert('Script {} has not had a successful run since {}'.format(script, last_finish_time))


def _alert_no_recent_records(script, first_finish_time):
    _alert('Script {} has not found any records to process since {}'.format(script, first_finish_time))


def run():
    import datetime
    start_time = timezone.now() + datetime.timedelta(days=10)
    print("Script {} starting at {}".format(SCRIPT, start_time))

    # get the last successful run for each script and check that it wasn't too long ago
    for script in update_existing_trials, download_new_trials:
        last_successful_run = ScriptRuns.objects.filter(
            script=script.SCRIPT, success=True).order_by('-finish_time').first()
        if last_successful_run:
            if (start_time - last_successful_run.finish_time).days > 5:
                _alert_no_recent_run(script.SCRIPT, last_successful_run.finish_time)

            # sum the record count for the last 10 successful runs and ensure it is >= 1
            last_10_successful_runs = ScriptRuns.objects.filter(
                script=script.SCRIPT, success=True).order_by('-finish_time')[:10]
            record_count = sum(run.record_count for run in last_10_successful_runs)
            if record_count == 0:
                _alert_no_recent_records(script.SCRIPT, [r for r in last_10_successful_runs][-1].finish_time)
        else:
            # if there are no successful runs at all, this is probably the very first time this
            # script has run, so just ignore it
            pass
