function LocationWidget() {
    this.name = 'locationWidget';
    this.templatePath = 'location_widget.html';
}

LocationWidget.prototype = Object.create(Page.prototype);
LocationWidget.prototype.render_data = function(data) {
    var page_render_data = Page.prototype.render_data.call(this, data);
    page_render_data.selected_locations = data.prefs.search.locations;
    var locations = {};
    data.trials.forEach(function (t) {
      if (t.locations) {
          t.locations.forEach(function (l) {
            var is_selected = page_render_data.selected_locations.indexOf(l) > -1;
            locations[l] = is_selected;
          });
      }
    });
    page_render_data.locations = [];
    for (var loc in locations) {
        if (locations.hasOwnProperty(loc)) {
            page_render_data.locations.push({'location': loc, 'selected': locations[loc]});
        }
    }
    page_render_data.locations.sort(
        function (a, b) {
            return a['location'] < b['location'] ? -1
                 : a['location'] > b['location'] ? 1
                 : 0
        }
    );
    page_render_data.matching_trials = Search(data.trials, data.prefs.search).length;
    return page_render_data;
};

LocationWidget.prototype.updateLocations = function(data) {
    var args = [0, data.selected_locations.length].concat($('[name=locations]').val());

    [].splice.apply(data.selected_locations, args)

    return true;
};
