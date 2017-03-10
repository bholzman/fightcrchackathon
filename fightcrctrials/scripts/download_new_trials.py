"""
Queries various clinical trials sources to find new updated/released clinical
trials from within the last week, and adds them to a google spreadsheet
to be curated/added to the main spreadhsheet

TODO(bkies):
 - Refactor to use existing codebase google api keys
 - Create a new spreadsheet each time and output the url for it
"""
from __future__ import print_function
import httplib2
import os
from sqlalchemy import create_engine, text

from apiclient import discovery
from oauth2client import client
from oauth2client import tools
from oauth2client.file import Storage

try:
    import argparse
    flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
except ImportError:
    flags = None

# If modifying these scopes, delete your previously saved credentials
# at ~/.credentials/sheets.googleapis.com-python-quickstart.json
SCOPES = 'https://www.googleapis.com/auth/spreadsheets'
CLIENT_SECRET_FILE = 'bens_client_secret.json'
APPLICATION_NAME = 'Google Sheets API Python Quickstart'

def get_credentials():
    """Gets valid user credentials from storage.

    If nothing has been stored, or if the stored credentials are invalid,
    the OAuth2 flow is completed to obtain the new credentials.

    Returns:
        Credentials, the obtained credential.
    """
    home_dir = os.path.expanduser('~')
    credential_dir = os.path.join(home_dir, '.credentials')
    if not os.path.exists(credential_dir):
        os.makedirs(credential_dir)
    credential_path = os.path.join(credential_dir,
                                   'sheets.googleapis.com-python-quickstart.json')

    store = Storage(credential_path)
    credentials = store.get()
    if not credentials or credentials.invalid:
        flow = client.flow_from_clientsecrets(CLIENT_SECRET_FILE, SCOPES)
        flow.user_agent = APPLICATION_NAME
        if flags:
            credentials = tools.run_flow(flow, store, flags)
        else: # Needed only for compatibility with Python 2.6
            credentials = tools.run(flow, store)
        print('Storing credentials to ' + credential_path)
    return credentials

def get_sql_string():
    return text("""
select st.nct_id
 , st.first_received_date as date_trial_added
 , st.brief_title
 , st.official_title
 , st.overall_status as program_status
 , 'Non-Immunotherapy CRC' as trial_type
 , st.phase as eligible_cancer_phases
 , el.minimum_age as minimum_age
 , el.maximum_age as maximum_age
 , el.gender as gender_criteria
 , el.criteria as eligibility_criteria
 , st.last_changed_date as last_changed_date
 --   , fac.locations
 , cont.contact_phones
 , cont.contact_emails
 , links.urls
 , array_agg(distinct int.name) as drug_names

from public.studies st
 join public.conditions cond
   on cond.nct_id = st.nct_id
 join public.interventions int
   on int.nct_id = st.nct_id
      and int.intervention_type = 'Drug'
 --   join (select fac.nct_id
 --           , array_agg(distinct (CASE WHEN country = 'United States' then fac.state else fac.country end)) as locations
 --         from public.facilities fac
 --         group by fac.nct_id) fac
 --     on fac.nct_id = st.nct_id
 left join (select cont.nct_id
              , array_agg(distinct cont.phone) as contact_phones
              , array_agg(distinct cont.email) as contact_emails
            from public.facility_contacts cont
            where cont.email is not NULL
                  and cont.phone is not null
            group by cont.nct_id) cont
   on cont.nct_id = st.nct_id
 left join (select links.nct_id
              , array_agg(url) as urls
            from public.links links
            where url is not NULL
            group by links.nct_id) links
   on links.nct_id = st.nct_id
 left join public.keywords ky
   on ky.nct_id = st.nct_id
 left join public.eligibilities el
   on el.nct_id = st.nct_id
-- all logic conditions
where st.study_type =  'Interventional'
     and phase in ('Phase 1/Phase 2','Phase 2','Phase 2/Phase 3','Phase 3','Phase 4')
     and overall_status in ('Recruiting','Enrolling by invitation','Not yet recruiting','Available')
     and (first_received_date >= date(current_date - 100000) OR st.last_changed_date >= date(current_date - 100000))
     --here we are checking for colon related trials
     and ((st.official_title ilike '%colorec%' or st.official_title ilike '%colon%'
           or st.official_title ilike '%rectum%' or st.official_title ilike '%rectal%'
           or st.official_title ilike '%CRC%' OR st.official_title ilike '%Advanced Cancer%')
          or (cond.name ilike '%colorec%' or cond.name ilike '%colon%'
              or cond.name ilike '%rectum%' or cond.name ilike '%rectal%'
              or cond.name ilike '%CRC%')
          or (ky.name ilike '%colorec%' or ky.name ilike '%colon%' or ky.name ilike '%rectum%'
              or ky.name ilike '%rectal%' or ky.name ilike '%CRC%'))
     --here we are checking for cancer related trails
     and ((st.official_title ilike '%cancer%' or st.official_title ilike '%neoplasm%')
          or (cond.name ilike '%cancer%' or cond.name ilike '%neoplasm%')
          or (ky.name ilike '%cancer%' or ky.name ilike '%neoplasm%')
          or (cond.name ilike '%advanced solid tumor%'))
group by 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15;
    """)


def get_range(rows):
    """returns an excel-based ranged for the cells, like A1:B2"""
    if len(rows) == 0 or len(rows[0]) == 0:
        return None

    end_row = len(rows) + 1
    end_col = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'[len(rows[0]) - 1]
    return "A1:{}{}".format(end_col, end_row)

def get_rows():
    rows = []
    engine = create_engine('postgresql://aact:aact@aact-prod.cr4nrslb1lw7.us-east-1.rds.amazonaws.com/aact')
    for row in engine.execute(get_sql_string()):
        rows.append(row)

    return rows

def get_header():
    return [
      'id',
      'date_trial_added',
      'brief_title',
      'official_title',
      'program_status',
      'trial_type',
      'eligible_cancer_phases',
      'minimum_age',
      'maximum_age',
      'gender_criteria',
      'last_changed_date',
      'contact_phones',
      'contact_emails',
      'urls',
      'drug_names',
    ]



def download_new_trials():

    credentials = get_credentials()
    http = credentials.authorize(httplib2.Http())
    discoveryUrl = ('https://sheets.googleapis.com/$discovery/rest?'
                    'version=v4')
    service = discovery.build('sheets', 'v4', http=http,
                              discoveryServiceUrl=discoveryUrl)

    spreadsheetId = '1uFg9BmRahFNUXO3ivDGh1y-ayKhWiE7sGFbR-m5F5qM'

    cells = get_rows()
    range_ = get_range(cells)
    header = get_header()

    body = {
        'values': [header] + [["%s" % c for c in row] for row in cells],
    }

    # update the spreedsheet
    service.spreadsheets().values().update(
        spreadsheetId=spreadsheetId,
        body=body,
        range=range_,
        valueInputOption='USER_ENTERED'
    ).execute()


if __name__ == '__main__':
    download_new_trials()