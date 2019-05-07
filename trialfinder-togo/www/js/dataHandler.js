function DataHandler(source) {
    this.source = source;
}

DataHandler.prototype.loadTrials = function() {
    var deferred = $.Deferred();
    $.ajax(this.source + 'trials-json/', {dataType: 'json'}).done(function(content) {
        var trials = [];
        for (var i = 0; i < content.length; i++) {
            var c = content[i];
            if (c.trial_link === undefined || c.trial_link === "") {
                c.trial_link = 'http://clinicaltrials.gov/ct2/show/' + c.nct_id;
            }
            trials.push(new Trial(
                c.nct_id, c.trial_link, c.is_crc_trial, c.is_immunotherapy_trial, c.subtype,
                c.prior_io_ok, c.comments, c.publications, c.urls, c.brief_title, c.title,
                c.program_status, c.locations, c.date_trial_added, c.updated_date, c.phase,
                c.intervention_types, c.drug_names, c.drug_brand_names, c.description, c.min_age,
                c.max_age, c.gender, c.inclusion_criteria, c.exclusion_criteria
            ));
        }
        window.localStorage.setItem("__fightcrc_trialfinder.trials", JSON.stringify(trials));

        deferred.resolve(trials);
    }).fail(function(){
        deferred.reject();
    });
    return deferred.promise();
};

DataHandler.prototype.loadFAQ = function() {
    var deferred = $.Deferred();
    $.ajax(this.source + 'mobile-faq-json/', {dataType: 'json'}).done(function(content) {
        var faqs = [];
        for (var i = 0; i < content.length; i++) {
            var c = content[i];
            faqs.push(new FAQItem(c.question, c.answer))
        }
        window.localStorage.setItem("__fightcrc_trialfinder.faqs", JSON.stringify(faqs));
        deferred.resolve(faqs);
    }).fail(function(){
        deferred.reject();
    });
    return deferred.promise();
};
