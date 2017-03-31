# FightCRC Trial Finder

This application provides an easy-to-use interface for colorectal cancer patients searching for clinical trials.

In addition to the public-facing search interface, there are several scheduled jobs that download new and updated
trials from clinicaltrials.gov. Actually, the trials are downloaded from the [AACT Database](https://aact-prod.herokuapp.com/).

When a new trial is downloaded, it is not immediately available in the search interface but must be manually reviewed
using the [built-in administrative interface](http://fightcrctrials.herokuapp.com/admin/fightcrctrials/crctrial/).

It is also possible to manually add trials that do not exist in clinicaltrials.gov using the administrative interface.


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


