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
            var trial = JSON.parse(JSON.stringify(t));
            if (trial.gender == 'A') {
                trial.gender = 'Male, Female';
            } else if (trial.gender == 'M') {
                trial.gender = 'Male';
            } else if (trial.gender == 'F') {
                trial.gender = 'Female';
            }
            page_render_data.trial = trial;
        }
    });
    return page_render_data;
};
