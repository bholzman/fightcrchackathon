var Search = function(trials, search) {
    var matching = [];
    trials.forEach(function (t) {
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
            }
        } else {
            matching.push(t);
        }

    });

    return matching;
};
