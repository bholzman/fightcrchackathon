"""
Updates our existing CRT trials with any new
information sourced from the aact datatbase.
"""

from __future__ import print_function
import datetime
import httplib2
import os

from sqlalchemy import create_engine, text


class CRTUpdater(object):
    def update_existing_trials(self):
        # query trials that we have
        updated_aac_trials = self.get_updated_aac_trials_map()

        # for each trial, update it's information
        for trial in Trial.objects.filter_by(nct_ids=aact_updated_trials.keys()):
            aact_trial = aact_updated_trials.fetch('nct_id')
            if aact_trial is None:
                continue

            trial.update(
                date_trial_added=aact_updated_trials['date_trial_added'],
                brief_title=aact_updated_trials['brief_title'],
                official_title=aact_updated_trials['official_title'],
                program_status=aact_updated_trials['program_status'],
                trial_type=aact_updated_trials['trial_type'],
                eligible_cancer_phases=aact_updated_trials['eligible_cancer_phases'],
                minimum_age=aact_updated_trials['minimum_age'],
                maximum_age=aact_updated_trials['maximum_age'],
                gender_criteria=aact_updated_trials['gender_criteria'],
                last_changed_date=aact_updated_trials['last_changed_date'],
                contact_phones=aact_updated_trials['contact_phones'],
                contact_emails=aact_updated_trials['contact_emails'],
                urls=aact_updated_trials['urls'],
                drug_names=aact_updated_trials['drug_names'],
            )

    def get_updated_aac_trials_map(self):
        """Returns a map of nct_ids to recently updated aact_trials from aact"""
        engine = create_engine('postgresql://aact:aact@aact-prod.cr4nrslb1lw7.us-east-1.rds.amazonaws.com/aact')
        trials = {}
        for row in engine.execute(self.get_sql_string()):
            trials[row['nct_id']] = row

        return trials

    def get_sql_string(self):
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

def run():
      CRTUpdater().update_existing_trials()
