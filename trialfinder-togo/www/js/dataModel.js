function Trial(trial_id, is_crc_trial, is_immunotherapy_trial, subtype,
               prior_io_ok, comments, publications, urls, brief_title, title, program_status,
               locations, date_trial_added, updated_date, phase, intervention_types,
               drug_names, drug_brand_names, description, min_age, max_age, gender,
               inclusion_criteria, exclusion_criteria) {
    this.trial_id = trial_id;
    this.is_crc_trial = is_crc_trial;
    this.is_immunotherapy_trial = is_immunotherapy_trial;
    this.subtype = subtype;
    this.prior_io_ok = prior_io_ok;
    this.comments = comments;
    this.publications = publications;
    this.urls = urls;
    this.brief_title = brief_title;
    this.title = title;
    this.program_status = program_status;
    this.locations = locations;
    this.date_trial_added = date_trial_added;
    this.updated_date = updated_date;
    this.phase = phase;
    this.intervention_types = intervention_types;
    this.drug_names = drug_names;
    this.drug_brand_names = drug_brand_names;
    if (description != '' && description != 'None') {
        this.description = convertDescriptionToParagraphs(description);
    } else {
        this.description = convertDescriptionToParagraphs(title);
    }
    this.min_age = min_age;
    this.max_age = max_age;
    this.gender = gender;
    this.inclusion_criteria = inclusion_criteria;
    this.exclusion_criteria = exclusion_criteria;
}

function Preferences(search, app) {
    console.assert($.isPlainObject(search));
    this.search = search;
    console.assert($.isPlainObject(app));
    this.app = app;
}

function Data(trials, prefs) {
    console.assert($.isArray(trials));
    this.trials = trials;
    console.assert(prefs instanceof Preferences);
    this.prefs = prefs;
}

Data.prototype.last_update = function() {
    var last_update = undefined
    for (var i = 0, l = this.trials.length; i < l; i++) {
        if (typeof last_update === 'undefined' || this.trials[i].updated_date > last_update) {
            last_update = this.trials[i].updated_date;
        }
    }
    return last_update;
};

function convertDescriptionToParagraphs(description) {
    // TODO - Refactor
    return description
            .split('\n')
            .map(s => s.trim())
            .map(s => s || '\n')
            .join(' ')
            .split('\n')
            .map(s => s.trim())
            .filter(s => !!s)
            .map(s => ({
                paragraph: s,
            }));
}
