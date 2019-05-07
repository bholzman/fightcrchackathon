function Trial(trial_id, trial_link, is_crc_trial, is_immunotherapy_trial, subtype,
               prior_io_ok, comments, publications, urls, brief_title, title, program_status,
               locations, date_trial_added, updated_date, phase, intervention_types,
               drug_names, drug_brand_names, description, min_age, max_age, gender,
               inclusion_criteria, exclusion_criteria) {
    this.trial_id = trial_id;
    this.trial_link = trial_link;
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

function FAQItem(question, answer) {
    this.question = question;
    this.answer = answer;
}

function Preferences(search, app) {
    console.assert($.isPlainObject(search));
    this.search = search;
    console.assert($.isPlainObject(app));
    this.app = app;
}

Preferences.prototype.save = function() {
    window.localStorage.setItem("__fightcrc_trialfinder.prefs.search", JSON.stringify(this.search));
    window.localStorage.setItem("__fightcrc_trialfinder.prefs.app", JSON.stringify(this.app));
};

Preferences.prototype.restore = function() {
    var savedSearch = window.localStorage.getItem("__fightcrc_trialfinder.prefs.search");
    if (savedSearch) {
        this.search = JSON.parse(savedSearch);
    } else {
        this.clearSearch();
    }

    var savedApp = window.localStorage.getItem("__fightcrc_trialfinder.prefs.app");
    if (savedApp) {
        this.app = JSON.parse(savedApp);
    } else {
        this.app = {'onTrialList': false, 'lastVisited': '0000-00-00', 'favorites': {}};
    }
};

Preferences.prototype.clearSearch = function() {
    this.search = {
        'hasImmunoTherapy': undefined,
        'doesKnowMsStatus': undefined,
        'hasPreviouslyUsedImmunoTherapy': undefined,
        'is_immunotherapy_trial': undefined,
        'prior_io_ok': undefined,
        'locations': [],
        'display_trials_outside_locations': false,
        'search': '',
        'recruitment_statuses': undefined,
        'phases': undefined,
        'date_added': undefined
    };
};

function Data(trials, faqs, prefs) {
    console.assert($.isArray(trials));
    this.trials = trials;
    console.assert($.isArray(faqs));
    this.faqs = faqs;
    console.assert(prefs instanceof Preferences);
    this.prefs = prefs;
    // set "favorite" attribute of trials that are in the "favorites" list
    var favorites = this.prefs.app.favorites || {};
    this.trials.forEach(function (t) {
        t.favorite = t.trial_id in favorites;
    });
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
    if (description === null || description === undefined) {
        description = ''
    }
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
