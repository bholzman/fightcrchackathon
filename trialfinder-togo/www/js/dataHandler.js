function DataHandler(source) {
    this.source = source;
}

DataHandler.prototype.loadTrials = function() {
    var deferred = $.Deferred();
    $.ajax(this.source + 'trials-json/', {dataType: 'json'}).done(function(content) {
        var trials = [];
        for (var i = 0; i < content.length; i++) {
            var c = content[i];
            trials.push(new Trial(
                c.nct_id, c.trial_link, c.is_crc_trial, c.is_immunotherapy_trial, c.subtype,
                c.prior_io_ok, c.comments, c.publications, c.urls, c.brief_title, c.title,
                c.program_status, c.locations, c.date_trial_added, c.updated_date, c.phase,
                c.intervention_types, c.drug_names, c.drug_brand_names, c.description, c.min_age,
                c.max_age, c.gender, c.inclusion_criteria, c.exclusion_criteria
            ));
        }
        deferred.resolve(trials);
    });
    return deferred.promise();
};
