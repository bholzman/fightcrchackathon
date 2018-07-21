var Search = function(trials, search) {
    var matching = [];
    trials.forEach(function (t) {
        if (search.prior_io_ok !== undefined) {
            if (t.prior_io_ok !== search.prior_io_ok) {
                return;
            }
        }

        if (search.is_immunotherapy_trial !== undefined) {
            if (t.is_immunotherapy_trial !== search.is_immunotherapy_trial) {
                return;
            }
        }

        if (search.recruitment_statuses) {
            if (!search.recruitment_statuses.includes(t.program_status)) {
                return;
            }
        }

        if (search.phases) {
            if (!search.phases.includes(t.phase)) {
                return;
            }
        }

        if (search.date_added) {
            if (t.date_trial_added < search.date_added) {
                return;
            }
        }

        if (search.therapy_names) {
            var names = search.therapy_names.split(new RegExp('\b'));
            var found = false;
            for (var i = 0; i < names.length && !found; i++) {
                var name = names[i].toUpperCase();
                if (t.drug_names) {
                    for (var j = 0; j < t.drug_names.length && !found; j++) {
                        if (t.drug_names[j].toUpperCase().includes(name)) {
                            found = true;
                        }
                    }
                }
                if (!found && t.drug_brand_names) {
                    for (var j = 0; j < t.drug_brand_names.length && !found; j++) {
                        if (t.drug_brand_names[j].toUpperCase().includes(name)) {
                            found = true;
                        }
                    }
                }
            }
            if (!found) {
                return;
            }
        }

        if (search.search) {
            var searchText = [
                t.trial_id, t.subtype, t.comments, t.publications, t.title, t.brief_title, t.drug_names, t.drug_brand_names, t.description
            ].join('|').toUpperCase();
            if (!searchText.includes(search.search.toUpperCase())) {
                return;
            }
        }
        if (t.locations) {
            var locationsMatch = false;
            for (var i = 0, l = t.locations.length; i < l; i++) {
                if (search.locations.indexOf(t.locations[i]) > -1) {
                    locationsMatch = true;
                    break;
                }
            }
            if (locationsMatch) {
                matching.push(t);
                t.matches_selected_locations = true;
            } else if (search.display_trials_outside_locations) {
                matching.push(t);
                t.matches_selected_locations = false;
            }
        } else {
            matching.push(t);
            t.matches_selected_locations = false;
        }

    });

    return matching;
};
