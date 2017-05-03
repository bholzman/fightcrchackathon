from sqlalchemy import and_, bindparam, case, create_engine, distinct, exists, literal, MetaData, or_, select, Table, union
from sqlalchemy.sql.expression import func

class AACT(object):
    def __init__(self):
        self.engine = create_engine('postgresql://aact:aact@aact-prod.cr4nrslb1lw7.us-east-1.rds.amazonaws.com/aact')
        self.meta = MetaData(bind=self.engine)

    def _table(self, name):
        if name in self.meta.tables:
            return self.meta.tables.get(name)
        return Table(name, self.meta, autoload=True)

    def studies(self):
        return self._table('studies')

    def conditions(self):
        return self._table('conditions')

    def interventions(self):
        return self._table('interventions')

    def facilities(self):
        return self._table('facilities')

    def facility_contacts(self):
        return self._table('facility_contacts')

    def links(self):
        return self._table('links')

    def detailed_descriptions(self):
        return self._table('detailed_descriptions')

    def keywords(self):
        return self._table('keywords')

    def eligibilities(self):
        return self._table('eligibilities')

    def mesh_terms(self):
        return self._table('mesh_terms')

    def browse_conditions(self):
        return self._table('browse_conditions')

    def trial_query(self):
        studies = self.studies()
        conditions = self.conditions()
        interventions = self.interventions()
        facilities = self.facilities()
        facility_contacts = self.facility_contacts()
        links = self.links()
        description = self.detailed_descriptions()
        keywords = self.keywords()
        eligibilities = self.eligibilities()
        nct_id = bindparam('nct_id')

        cond_query = select([
            conditions.c.nct_id,
            func.array_agg(
                distinct(conditions.c.name)
            ).label('conditions')
        ]).where(
            conditions.c.nct_id == nct_id
        ).group_by(conditions.c.nct_id).alias('cond_query')

        intervention_query = select([
            interventions.c.nct_id,
            func.array_agg(
                distinct(interventions.c.intervention_type + ': ' + interventions.c.name)
            ).label('interventions')
        ]).where(
            interventions.c.nct_id == nct_id
        ).group_by(interventions.c.nct_id).alias('intervention_query')

        loc_query = select([
            facilities.c.nct_id,
            func.array_agg(
                distinct(
                    case([(facilities.c.country == 'United States', facilities.c.state)],
                         else_=facilities.c.country)
                )
            ).label('locations')
        ]).where(
            facilities.c.nct_id == nct_id
        ).group_by(facilities.c.nct_id).alias('loc_query')

        email_phone_query = select([
            facility_contacts.c.nct_id,
            func.array_agg(
                distinct(facility_contacts.c.phone)
            ).label('contact_phones'),
            func.array_agg(
                distinct(facility_contacts.c.email)
            ).label('contact_emails')
        ]).where(
            and_(
                facility_contacts.c.nct_id == nct_id,
                or_(
                    facility_contacts.c.phone.isnot(None),
                    facility_contacts.c.email.isnot(None)
                )
            )
        ).group_by(
            facility_contacts.c.nct_id
        ).alias('email_phone_query')

        link_query = select([
            links.c.nct_id,
            func.array_agg(
                distinct(links.c.url)
            ).label('urls')
        ]).where(
            and_(
                links.c.url.isnot(None),
                links.c.nct_id == nct_id
            )
        ).group_by(
            links.c.nct_id
        ).alias('link_query')

        drug_query = select([
            interventions.c.nct_id,
            func.array_agg(
                distinct(interventions.c.name)
            ).label('drug_names')
        ]).where(
            and_(
                interventions.c.intervention_type.in_(['Drug', 'Device', 'Biological']),
                interventions.c.nct_id == nct_id
            )
        ).group_by(
            interventions.c.nct_id
        ).alias('drug_query')

        return select([
            studies.c.nct_id,
            studies.c.first_received_date.label('date_trial_added'),
            studies.c.brief_title,
            studies.c.official_title,
            studies.c.overall_status.label('program_status'),
            studies.c.phase.label('eligible_cancer_phase'),
            eligibilities.c.minimum_age.label('minimum_age'),
            eligibilities.c.maximum_age.label('maximum_age'),
            eligibilities.c.gender.label('gender_criteria'),
            func.trim(func.regexp_replace(
                eligibilities.c.criteria,
                # capture from the start of the inclusion section up until the first exclusion section
                # Note - the (.*?) is separated from the "inclusion" capture because otherwise the postgres
                # engine (9.5) did not handle the non-greedy operator properly
                '.*(Inclusion|Major inclusion|INCLUSION|Eligibility Criteria)(.*?)'
                '(Exclusion|Major exclusion|EXCLUSION).*',
                '\\1\\2')).label('inclusion_criteria'),
            func.trim(func.regexp_replace(
                eligibilities.c.criteria,
                # capture from the first exclusion section to the end
                '.*?((?:Exclusion|Major exclusion|EXCLUSION).*)',
                '\\1')).label('exclusion_criteria'),
            studies.c.last_changed_date,
            loc_query.c.locations,
            email_phone_query.c.contact_phones,
            email_phone_query.c.contact_emails,
            link_query.c.urls,
            description.c.description.label('trial_description'),
            drug_query.c.drug_names,
        ]).select_from(
            studies.outerjoin(
                loc_query, loc_query.c.nct_id == studies.c.nct_id
            ).outerjoin(
                email_phone_query, email_phone_query.c.nct_id == studies.c.nct_id
            ).outerjoin(
                link_query, link_query.c.nct_id == studies.c.nct_id
            ).outerjoin(
                eligibilities, eligibilities.c.nct_id == studies.c.nct_id
            ).outerjoin(
                description, description.c.nct_id == studies.c.nct_id
            ).outerjoin(
                drug_query, drug_query.c.nct_id == studies.c.nct_id
            )
        ).where(studies.c.nct_id == nct_id)

    def add_crc_classifier(self, query):
        studies = self.studies()
        keywords = self.keywords()
        conditions = self.conditions()
        nct_id = bindparam('nct_id')

        terms = ['colorec', 'colon', 'rectum', 'rectal', 'CRC']
        fields = [studies.c.official_title, conditions.c.name, keywords.c.name]

        cases = [(or_(field.ilike('%' + term + '%') for term in terms for field in fields), 1)]

        is_crc_trial = select([
            studies.c.nct_id,
            func.max(case(cases, else_=0)).label('is_crc_trial')
        ]).select_from(
            studies.outerjoin(
                keywords, keywords.c.nct_id == studies.c.nct_id
            ).outerjoin(
                conditions, conditions.c.nct_id == studies.c.nct_id
            )
        ).where(
            studies.c.nct_id == nct_id
        ).group_by(studies.c.nct_id).alias('is_crc_trial')

        return query.column(
            is_crc_trial.c.is_crc_trial
        ).select_from(
            query.froms[0].join(is_crc_trial, is_crc_trial.c.nct_id == studies.c.nct_id)
        )

    def add_io_classifier(self, query):
        studies = self.studies()
        interventions = self.interventions()
        keywords = self.keywords()
        descriptions = self.detailed_descriptions()
        eligibilities = self.eligibilities()
        nct_id = bindparam('nct_id')

        terms = ['pd1', 'pd-1', 'pdl1', 'pdl-1', 'pd(L)1', 'ctla4', 'ctla-4', 'nivo', 'pembro', 'atezo', 'ipilimumab',
                 'immunotherapy', 'cell therapy', 'CAR-T', 'CART', 'MEDI4736', 'durva', 'avelu', 'LAG525', 'MK-3475',
                 'opdivo', 'keytruda', 'Provenge', 'sipuleucel', 'Axicabtagene', 'Ciloleucel', 'CTL019',
                 'tisagenlecleucel-T', 'MGB453', 'NY-ESO', 'SPEAR']

        # generate separate subqueries for each field
        fields = [
            (studies, 'official_title'),
            (interventions, 'name'),
            (keywords, 'name'),
            (descriptions, 'description'),
        ]

        clauses = []
        for table, field_name in fields:
            field = getattr(table.c, field_name)
            cases = or_(field.ilike('%' + term + '%') for term in terms)
            clause = select([
                literal(True)
            ]).where(
                and_(table.c.nct_id == nct_id, cases)
            )
            if table is interventions:
                clause = clause.where(
                    interventions.c.intervention_type.in_(['Drug', 'Device', 'Biological'])
                )
            clauses.append(clause)

        exclusion_terms = ['autoimmune', 'auto-immune', 'immunotherapy', 'immune', 'pd-1', 'pd1']
        cases = or_(
            func.trim(func.regexp_replace(
                eligibilities.c.criteria,
                '.*?((?:Exclusion|Major exclusion|EXCLUSION).*)',
                '\\1')).ilike('%' + term + '%') for term in exclusion_terms)

        clauses.append(
            select([
                literal(True)
            ]).where(
                and_(eligibilities.c.nct_id == nct_id, cases)
            )
        )

        return query.column(
            or_(exists(clause) for clause in clauses).label('is_immunotherapy_trial')
        )

    def newly_added_trials(self, cutoff_days):
        studies = self.studies()
        conditions = self.conditions()
        keywords = self.keywords()
        terms = ['cancer', 'neoplasm', 'tumor', 'tumour', 'malignan', 'carcinoma', 'metast']
        fields = [studies.c.official_title, conditions.c.name, keywords.c.name]
        term_clauses = [field.ilike('%' + term + '%') for field in fields for term in terms]

        return select([
            distinct(studies.c.nct_id)
        ]).select_from(
            studies.outerjoin(
                conditions, conditions.c.nct_id == studies.c.nct_id
            ).outerjoin(
                keywords, keywords.c.nct_id == studies.c.nct_id
            )
        ).where(
            and_(
                studies.c.created_at >= func.date(func.current_date() - cutoff_days),
                studies.c.first_received_date >= '2017-02-01',
                studies.c.study_type == 'Interventional',
                studies.c.overall_status.in_([
                    'Recruiting','Enrolling by invitation','Not yet recruiting','Available']),
                or_(*term_clauses)
            )
        )

    def add_newly_updated_condition(self, query, cutoff_days, stub_ids):
        studies = self.studies()
        return query.where(
            or_(studies.c.updated_at >= func.date(func.current_date() - cutoff_days),
                studies.c.nct_id.in_(stub_ids))
        )
