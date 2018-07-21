function TrialList() {
    this.name = 'trialList';
    this.templatePath = 'trial_list.html';
}

TrialList.prototype = Object.create(Page.prototype);

TrialList.prototype.trials = function(data) {
    return Search(data.trials, data.prefs.search);
}

TrialList.prototype.render_data = function(data) {
    var page_render_data = Page.prototype.render_data.call(this, data);
    var lastVisited = data.prefs.app.lastVisited;
    data.trials.forEach(function (t) {
        t['new'] = t.date_trial_added >= lastVisited ? 'NEW' : t.updated_date >= lastVisited ? 'UPDATED' : '';
    });

    if (data.pageArgs[0] == 'clearSearch') {
        data.prefs.search.search = undefined;
    }

    var matching_trials = this.trials(data);

    matching_trials.forEach(function (t) {
        if (t.locations) {
            t['matched_location'] = t.locations[0];
            for (var i = 0; i < t.locations.length; i++) {
                var l = t.locations[i];
                if (data.prefs.search.locations.indexOf(l) > -1) {
                    t['matched_location'] = l;
                    break;
                }
            }
        } else {
            t['matched_location'] = 'N/A';
        }
    });

    page_render_data.search = data.prefs.search.search;

    page_render_data.trials = matching_trials.sort(
        function(a, b) {
            return a.matches_selected_locations && !b.matches_selected_locations 
                ? -1
                : b.matches_selected_locations && !a.matches_selected_locations
                  ? 1
                  : a.date_trial_added > lastVisited && b.date_trial_added <= lastVisited
                    ? -1
                    : b.date_trial_added > lastVisited && a.date_trial_added <= lastVisited
                      ? 1
                      : a.updated_date > b.updated_date
                        ? -1
                        : b.updated_date > a.updated_date
                          ? 1
                          : a.trial_id > b.trial_id
                            ? 1
                            : b.trial_id > a.trial_id
                              ? -1
                              : 0 });

    page_render_data.count = matching_trials.length;

    if (data.prefs.search.search) {
        page_render_data.search_selected = '-selected';
    } else {
        page_render_data.home_selected = '-selected';
    }
    return page_render_data;
};

TrialList.prototype.after_render = function(data) {
    data.prefs.app.onTrialList = true;

    var visitDate = new Date();
    data.prefs.app.lastVisited = visitDate.toISOString().slice(0, 10);
    data.prefs.save();
    if (this.last_selected_trial) {
        $('#trial-' + this.last_selected_trial).get(0).scrollIntoView();
    }
};

TrialList.prototype.selectTrial = function(data, id) {
    this.last_selected_trial = id;
    data.trials.forEach(function (t) {
        if (t['trial_id'] === id) {
            t['selected'] = !t['selected'];
        } else {
            delete t['selected'];
        }
    });
    return true;
};
