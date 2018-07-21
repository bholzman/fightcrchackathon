function TrialView() {
    this.name = 'trialView';
    this.templatePath = 'trial_view.html';
}

TrialView.prototype = Object.create(Page.prototype);
TrialView.prototype.render_data = function(data) {
    var page_render_data = Page.prototype.render_data.call(this, data);
    var trial_id = data.pageArgs[0];
    data.trials.forEach(function (t) {
        if (t.trial_id === trial_id) {
            page_render_data.orig_trial = t;
            var trial = JSON.parse(JSON.stringify(t));
            if (trial.gender == 'A') {
                trial.gender = 'Male, Female';
            } else if (trial.gender == 'M') {
                trial.gender = 'Male';
            } else if (trial.gender == 'F') {
                trial.gender = 'Female';
            }

            if (trial.locations == null) {
                trial.locations = 'N/A';
            }

            page_render_data.trial = trial;
        }
    });
    page_render_data.prefs = data.prefs;
    return page_render_data;
};

TrialView.prototype.toggleFavorite = function(data, trial_id) {
    if (data.trial.favorite) {
        data.orig_trial.favorite = false;
        delete data.prefs.app.favorites[trial_id];
    } else {
        data.orig_trial.favorite = true;
        data.prefs.app.favorites[trial_id] = true;
    }

    data.prefs.save();

    return true;
};
