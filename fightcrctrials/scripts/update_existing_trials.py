"""
Updates our existing CRT trials with any new
information sourced from the aact datatbase.
"""
from __future__ import print_function
import datetime
import httplib2
import os
import pickle

from sqlalchemy import create_engine, text
from fightcrctrials.models import CRCTrial
from fightcrctrials.serializers import AACTrialSerializer



class CRCTrialsUpdater(object):
    def __init__(self, use_pickle):
        self.use_pickle = use_pickle

    def update_existing_trials(self):
        # query trials that we have
        updated_aac_trials_map = self.get_updated_aac_trials_map()

        # for each trial, update it's information
        for trial in CRCTrial.objects.filter(nct_id__in=updated_aac_trials_map.keys()):
            aact_trial = updated_aac_trials_map.get(trial.nct_id)
            if aact_trial is None:
                continue

            serialized_aac_trial = AACTrialSerializer(aact_trial).serialize()

            trial.updated_date = serialized_aac_trial['updated_date']
            trial.date_trial_added = serialized_aac_trial['date_trial_added']
            trial.brief_title = serialized_aac_trial['brief_title']
            trial.title = serialized_aac_trial['title']
            trial.program_status = serialized_aac_trial['program_status']
            trial.phase = serialized_aac_trial['phase']
            trial.min_age = serialized_aac_trial['min_age']
            trial.max_age = serialized_aac_trial['max_age']
            trial.gender = serialized_aac_trial['gender']
            trial.inclusion_criteria = serialized_aac_trial['inclusion_criteria']
            trial.exclusion_criteria = serialized_aac_trial['exclusion_criteria']
            trial.locations = serialized_aac_trial['locations']
            trial.contact_phones = serialized_aac_trial['contact_phones']
            trial.contact_emails = serialized_aac_trial['contact_emails']
            trial.urls = serialized_aac_trial['urls']
            trial.description = serialized_aac_trial['description']
            trial.is_crc_trial = serialized_aac_trial['is_crc_trial']
            trial.is_immunotherapy_trial = serialized_aac_trial['is_immunotherapy_trial']
            trial.drug_names = serialized_aac_trial['drug_names']
            trial.save()


    def get_updated_aac_trials_map(self):
        """Returns a map of nct_ids to recently updated aact_trials from aact"""
        trials = {}
        for row in self.get_updated_aac_trials():
            trials[row['nct_id']] = row

        return trials

    def get_updated_aac_trials(self):
        """Returns a map of nct_ids to recently updated aact_trials from aact"""
        engine = create_engine('postgresql://aact:aact@aact-prod.cr4nrslb1lw7.us-east-1.rds.amazonaws.com/aact')

        pickle_file_path = 'data.pkl'
        if self.use_pickle and os.path.exists(pickle_file_path):
            with open(pickle_file_path, 'rb') as output:
                data = pickle.load(output)

            return data
        else:
            data = engine.execute(self.get_sql_string())
            if self.use_pickle:
                with open(pickle_file_path, 'wb') as output:
                    pickle.dump([a for a in data], output)
            return data

    def get_sql_string(self):
        return text("""
            select st.nct_id
              , st.first_received_date as date_trial_added
              , st.brief_title
              , st.official_title
              , st.overall_status as program_status
              , st.phase as eligible_cancer_phase
              , el.minimum_age as minimum_age
              , el.maximum_age as maximum_age
              , el.gender as gender_criteria
              , TRIM(regexp_replace(substring(el.criteria from position('Inclusion' in el.criteria) for position('Exclusion' in el.criteria)), 'Exclusion', '')) as inclusion_criteria
              , TRIM(substring(el.criteria from position('Exclusion' in el.criteria) for char_length(el.criteria))) as exclusion_criteria
              , st.last_changed_date as last_changed_date
              , fac.locations
              , cont.contact_phones
              , cont.contact_emails
              , links.urls
              , des.description as trial_description
              , (case when (((st.official_title ilike '%colorec%' or st.official_title ilike '%colon%'
                             or st.official_title ilike '%rectum%' or st.official_title ilike '%rectal%'
                             or st.official_title ilike '%CRC%')
                            or (cond.name ilike '%colorec%' or cond.name ilike '%colon%'
                                or cond.name ilike '%rectum%' or cond.name ilike '%rectal%'
                                or cond.name ilike '%CRC%')
                            or (ky.name ilike '%colorec%' or ky.name ilike '%colon%' or ky.name ilike '%rectum%'
                                or ky.name ilike '%rectal%' or ky.name ilike '%CRC%')) AND st.phase in ('Phase 1/Phase 2','Phase 2','Phase 2/Phase 3','Phase 3','Phase 4')) then True else False end) is_crc_trial
              , (case when      -- can you find the treatment in the title?
              ((st.official_title ilike '%pd1%' or st.official_title ilike '%pd-1%' or st.official_title ilike '%pdl1%' or st.official_title ilike '%pd-l1%'
                or st.official_title ilike '%ctla4%' or st.official_title ilike '%ctla-4%' or st.official_title ilike '%nivo%' or st.official_title ilike '%pembro%' or st.official_title ilike '%atezo%'
                or st.official_title ilike '%ipilimumab%' or st.official_title ilike '%immunotherapy%' or st.official_title ilike '%cell therapy%' or st.official_title ilike '%CAR-T%' or st.official_title ilike '%CART%'
                or st.official_title ilike '%MEDI4736%' or st.official_title ilike '%durva%' or st.official_title ilike '%avelu%' or st.official_title ilike '%LAG525%' or st.official_title ilike '%MK-3475%')
               -- can you find the treatment in the intervention?
               or (int.name ilike '%pd1%' or int.name ilike '%pd-1%' or int.name ilike '%pdl1%' or int.name ilike '%pd-l1%' or int.name ilike '%pd(L)1%' or int.name ilike '%cell therapy%' or int.name ilike '%CAR-T%'
                   or int.name ilike '%ctla4%' or int.name ilike '%ctla-4%' or int.name ilike '%nivo%' or int.name ilike '%pembro%' or int.name ilike '%ipilimumab%' or int.name ilike '%immunotherapy%' or int.name ilike '%CART%'
                   or int.name ilike '%atezo%' or int.name ilike '%MEDI4736%' or int.name ilike '%durva%' or int.name ilike '%avelu%' or int.name ilike '%LAG525%' or int.name ilike '%MK-3475%')
               -- can you find the treatment in the keyword?
               or (ky.name ilike '%pd1%' or ky.name ilike '%pd-1%' or ky.name ilike '%pdl1%' or ky.name ilike '%pd-l1%' or ky.name ilike '%pd(L)1%' or ky.name ilike '%ctla4%' or ky.name ilike '%ctla-4%' or ky.name ilike '%CAR-T%'
                   or ky.name ilike '%nivo%' or ky.name ilike '%pembro%' or ky.name ilike '%ipilimumab%' or ky.name ilike '%immunotherapy%' or ky.name ilike '%cell therapy%' or ky.name ilike '%CART%'
                   or ky.name ilike '%atezo%' or ky.name ilike '%MEDI4736%' or ky.name ilike '%durva%' or ky.name ilike '%avelu%' or ky.name ilike '%LAG525%' or ky.name ilike '%MK-3475%')
               -- can you find the treatment in the detailed description?
               or (des.description ilike '%pd1%' or des.description ilike '%pd-1%' or des.description ilike '%pdl1%' or des.description ilike '%pd-l1%' or des.description ilike '%pd(L)1%' or des.description ilike '%ctla4%' or des.description ilike '%ctla-4%' or des.description ilike '%CAR-T%'
                   or des.description ilike '%nivo%' or des.description ilike '%pembro%' or des.description ilike '%ipilimumab%' or des.description ilike '%immunotherapy%' or des.description ilike '%cell therapy%' or des.description ilike '%CART%'
                   or des.description ilike '%atezo%' or des.description ilike '%MEDI4736%' or des.description ilike '%durva%' or des.description ilike '%avelu%' or des.description ilike '%LAG525%' or des.description ilike '%MK-3475%')
               -- can you find XYZ on the exclusion criteria
               or (TRIM(substring(el.criteria from position('Exclusion' in el.criteria) for char_length(el.criteria)))) ilike '%autoimmune%'
               or (TRIM(substring(el.criteria from position('Exclusion' in el.criteria) for char_length(el.criteria)))) ilike '%auto-immune%'
               or (TRIM(substring(el.criteria from position('Exclusion' in el.criteria) for char_length(el.criteria)))) ilike '%immunotherapy%'
               or ((TRIM(substring(el.criteria from position('Exclusion' in el.criteria) for char_length(el.criteria)))) ilike '%immune%')
               or ((TRIM(substring(el.criteria from position('Exclusion' in el.criteria) for char_length(el.criteria)))) ilike '%pd-1%')
               or ((TRIM(substring(el.criteria from position('Exclusion' in el.criteria) for char_length(el.criteria)))) ilike '%pd1%')
              ) then True else False end) as is_immunotherapy_trial
              , '' as comments
              , '' as publications
              , array_agg(distinct int.name) as drug_names
            from public.studies st
              join public.conditions cond
                on cond.nct_id = st.nct_id
              join public.interventions int
                on int.nct_id = st.nct_id
                   and int.intervention_type in ('Drug', 'Device', 'Biology')
              join (select fac.nct_id
                      , array_agg(distinct (CASE WHEN country = 'United States' then fac.state else fac.country end)) as locations
                    from public.facilities fac
                    group by fac.nct_id) fac
                on fac.nct_id = st.nct_id
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
              left join public.detailed_descriptions des
                on des.nct_id = st.nct_id
              left join public.keywords ky
                on ky.nct_id = st.nct_id
              left join public.eligibilities el
                on el.nct_id = st.nct_id
            -- all logic conditions
            where st.study_type =  'Interventional'
              and overall_status in ('Recruiting','Enrolling by invitation','Not yet recruiting','Available')
              and ((st.official_title ilike '%cancer%' or st.official_title ilike '%neoplasm%' or st.official_title ilike '%tumor%')
                   or (cond.name ilike '%cancer%' or cond.name ilike '%neoplasm%' or cond.name ilike '%tumor%')
                   or (ky.name ilike '%cancer%' or ky.name ilike '%neoplasm%' or ky.name ilike '%tumor%')
                   or (cond.name ilike '%tumor%') or st.official_title ilike '%Advanced Cancer%' or (cond.name ilike '%advanced solid tumor%'))
              and (first_received_date >= date('2010-01-01'))
            group by 1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16,17,18,19;
                """)

def run(use_pickle=False):
    CRCTrialsUpdater(use_pickle).update_existing_trials()
