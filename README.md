# FightCRC Trial Finder

This application provides an easy-to-use interface for colorectal cancer patients searching for clinical trials.

In addition to the public-facing search interface, there are several scheduled jobs that download new and updated
trials from clinicaltrials.gov. Actually, the trials are downloaded from the [AACT Database](https://aact-prod.herokuapp.com/).

When a new trial is downloaded, it is not immediately available in the search interface but must be manually reviewed
using the [built-in administrative interface](http://fightcrctrials.herokuapp.com/admin/fightcrctrials/crctrial/).

It is also possible to manually add trials that do not exist in clinicaltrials.gov using the administrative interface.

This application is written in Python using the Django framework.

## Running Locally

Make sure you have Python [installed properly](http://install.python-guide.org).  Also, install the [Heroku Toolbelt](https://toolbelt.heroku.com/) and [Postgres](https://devcenter.heroku.com/articles/heroku-postgresql#local-setup).

```sh
$ heroku git:clone -a fightcrctrials
$ cd fightcrctrials
$ virtualenv venv
$ source venv/bin/activate
$ pip install -r requirements.txt

$ createdb fightcrctrials

$ python manage.py migrate
$ python manage.py collectstatic

$ heroku local
```

Your app should now be running on [localhost:5000](http://localhost:5000/).

## Deploying to Heroku

```sh
$ git push heroku master

$ heroku run python manage.py migrate
$ heroku open
```
or

[![Deploy](https://www.herokucdn.com/deploy/button.png)](https://heroku.com/deploy)

## Documentation

For more information about using Python on Heroku, see these Dev Center articles:

- [Python on Heroku](https://devcenter.heroku.com/categories/python)

Here is a listing of the important files in this repository and a description of each:

app/settings.py                                     - Django settings file
app/urls.py                                         - Django URL routes
app/wsgi.py                                         - WSGI config for app
app.json                                            - Heroku app descriptor
bin/check_script_runs                               - Wrapper for scheduled job to check health of update process
bin/download_new_trials                             - Wrapper for scheduled job to download new trials
bin/update_existing_trials                          - Wrapper for scehduled job to look for updates to trials
fightcrctrials/aact.py                              - Interface to AACT database; logic for trial download is here
fightcrctrials/admin.py                             - Configuration of the administrative interface
fightcrctrials/email.py                             - Helper for sending emails (uses sendgrid to send emails)
fightcrctrials/forms.py                             - Django form for the Contact Us page
fightcrctrials/migrations                           - Database migrations live here
fightcrctrials/models.py                            - Data models live here
fightcrctrials/scripts/check_script_runs.py         - Script to check health of update process
fightcrctrials/scripts/download_new_trials.py       - Script to download new trials
fightcrctrials/scripts/trial_importer.py            - Library used by download and update scripts
fightcrctrials/scripts/update_existing_trials.py    - Script to update existing trials
fightcrctrials/serializers.py                       - Contains data serializers
fightcrctrials/signals.py                           - Django signal handler for creating DeletedCRCTrial records
                                                      when a CRCTrial is deleted; this prevents the download new
                                                      trials script from re-downloading trials that have been
                                                      reviewed and manually deleted as irrelevant
fightcrctrials/static                               - Static css, js and images go here. Most of the files here are
                                                      third-party content.
fightcrctrials/templates/base.html                  - Base page template; other page templates inherit from this
fightcrctrials/templates/contactus.html             - The Contact Us page
fightcrctrials/templates/faq.html                   - The FAQ page
fightcrctrials/templates/index.html                 - The search result display page
fightcrctrials/templates/welcome.html               - The landing and search page
fightcrctrials/templatetags/user_text.py            - A custom template tag is defined here for bits of text that
                                                      can be edited using the administrative interface
fightcrctrials/views.py                             - Views for the app are defined here
newrelic.ini                                        - Configuration for New Relic (web monitoring)
