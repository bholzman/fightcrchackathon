from fightcrctrials.models import CRCTrial
from fightcrctrials.serializers import AACTrialSerializer

def update_or_create(record, include_classifiers=False):
    trial = AACTrialSerializer(record, classifiers=include_classifiers).serialize()
    defaults = {
        'updated_date': trial['updated_date'],
        'date_trial_added': trial['date_trial_added'],
        'brief_title': trial['brief_title'],
        'title': trial['title'],
        'program_status': trial['program_status'],
        'phase': trial['phase'],
        'min_age': trial['min_age'],
        'max_age': trial['max_age'],
        'gender': trial['gender'],
        'inclusion_criteria': trial['inclusion_criteria'],
        'exclusion_criteria': trial['exclusion_criteria'],
        'locations': trial['locations'],
        'contact_phones': trial['contact_phones'],
        'contact_emails': trial['contact_emails'],
        'urls': trial['urls'],
        'description': trial['description'],
        'drug_names': trial['drug_names'],
        'conditions': trial['conditions'],
    }
    if include_classifiers:
        defaults['is_crc_trial'] = trial['is_crc_trial']
        defaults['is_immunotherapy_trial'] = trial['is_immunotherapy_trial']

    CRCTrial.objects.update_or_create(nct_id=record.nct_id, defaults=defaults)
