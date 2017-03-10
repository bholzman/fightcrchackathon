class AACTrialSerializer(object):
    """Serialzizes an AACT trial object into a dictionary of attributes used
    by a CRCTrial object"""
    def __init__(self, aact_trial):
        self.aact_trial = aact_trial

    def serialize(self):
       aact_trial = self.aact_trial
       return {
            'updated_date': aact_trial.last_changed_date,
            'date_trial_added': aact_trial.date_trial_added,
            'brief_title': self.truncate_or_none(aact_trial.brief_title),
            'title': self.truncate_or_none(aact_trial.official_title),
            'program_status': "%s" % aact_trial.program_status,
            'phase': "%s" % aact_trial.eligible_cancer_phase,
            'min_age': self.sanitize_min_age(aact_trial.minimum_age),
            'max_age': self.sanitize_max_age(aact_trial.maximum_age),
            'gender': self.sanitize_gender(aact_trial.gender_criteria),
            'inclusion_criteria': self.truncate_or_none(aact_trial.inclusion_criteria),
            'exclusion_criteria': self.truncate_or_none(aact_trial.exclusion_criteria),
            'locations': self.sanitize_locations(aact_trial.locations),
            'contact_phones': self.sanitize_phones(aact_trial.contact_phones),
            'contact_emails': self.sanitize_emails(aact_trial.contact_emails),
            'urls': self.sanitize_urls(aact_trial.urls),
            'description': "%s" % aact_trial.trial_description,
            'is_crc_trial': aact_trial.is_crc_trial,
            'is_immunotherapy_trial': aact_trial.is_immunotherapy_trial,
            'drug_names': self.sanitize_drug_names(aact_trial.drug_names),
        }

    def sanitize_urls(self, urls):
        if urls is None: return None

        return ["%s" % url[:200] for url in urls]

    def sanitize_phones(self, phones):
        if phones is None: return None

        return ["%s" % phone for phone in phones]

    def sanitize_emails(self, emails):
        if emails is None: return None

        return ["%s" % email for email in emails]

    def sanitize_locations(self, locations):
        if locations is None: return None

        return ["%s" % location for location in locations]


    def sanitize_gender(self, gender):
        if gender is None: return None

        if gender == 'Female':
          return "F"
        elif gender == 'Male':
          return 'M'
        elif gender == "All":
          return "A"
        else:
          # TODO(Bkies): add more gender types
          raise Exception("%s is not a valid gender" % gender)
          return None

    def truncate_or_none(self, string):
        if string is None: return "UNKOWN"
        return "%s" % string[:200]

    def sanitize_drug_names(self, drug_names):
        if drug_names is None: return None

        return ["%s" % drug for drug in drug_names]

    def sanitize_min_age(self, minimum_age):
        if minimum_age is None:
            return None

        try:
            int(minimum_age)
        except ValueError:
            return None

    def sanitize_max_age(self, maximum_age):
        if maximum_age is None:
            return None

        try:
            int(maximum_age)
        except ValueError:
            return None
