var Search = function(trials, search) {
    var matching = [];
    trials.forEach(function (t) {
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
