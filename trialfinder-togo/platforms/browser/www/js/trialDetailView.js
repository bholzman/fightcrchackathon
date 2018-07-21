function TrialDetailView() {
    this.name = 'trialDetailView';
    this.templatePath = 'trial_detail_view.html';
}

TrialDetailView.prototype = Object.create(Page.prototype);
TrialDetailView.prototype.render_data = function(data) {
    var page_render_data = Page.prototype.render_data.call(this, data);
    var trial_id = data.pageArgs[0];
    var field = data.pageArgs[1];
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
            page_render_data.detail = trial[field];
            page_render_data.title = field;
            page_render_data.trial_id = trial_id;
        }
    });
    return page_render_data;
};
