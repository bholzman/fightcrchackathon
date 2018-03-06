function TrialList() {
    this.name = 'trialList';
    this.templatePath = 'trial_list.html';
}

TrialList.prototype = Object.create(Page.prototype);
TrialList.prototype.render_data = function(data) {
    var page_render_data = Page.prototype.render_data.call(this, data);
    var lastVisited = data.prefs.app.lastVisited;
    data.trials.forEach(function (t) {
        t['new'] = t.date_trial_added > lastVisited ? '[NEW]' : t.updated_date > lastVisited ? '[UPDATED]' : '';
    });
    page_render_data.trials = data.trials.sort(
        function(a, b) {
            return a.updated_date > b.updated_date
                   ? -1
                   : b.updated_date > a.updated_date
                     ? 1
                     : a.trial_id > b.trial_id
                       ? 1
                       : b.trial_id > a.trial_id
                         ? -1
                         : 0 });
    page_render_data.count = data.trials.length;
    return page_render_data;
};

TrialList.prototype.selectTrial = function(data, id) {
    data.trials.forEach(function (t) {
        if (t['trial_id'] === id) {
            t['selected'] = !t['selected'];
        } else {
            delete t['selected'];
        }
    });
    return true;
};
