function FilterLocations() {
    this.name = 'filter-locations';
    this.templatePath = 'filter_locations.html';
    this.locationWidgetPage = new LocationWidget();
    var that = this;
    $.ajax(this.locationWidgetPage.templatePath).done(function (content) {
        Mustache.parse(content);
        that.locationWidget = content;
    });
}

FilterLocations.prototype = Object.create(Page.prototype);
FilterLocations.prototype.render_data = function(data) {
    var page_render_data = Page.prototype.render_data.call(this, data);
    page_render_data = Object.assign(page_render_data, this.locationWidgetPage.render_data(data));
    page_render_data.filters_selected = '-selected';
    return page_render_data;
};

FilterLocations.prototype.dependencies = function(render_data) {
    return Object.assign(Page.prototype.dependencies.call(this, render_data),
        {locationWidget: Mustache.render(this.locationWidget, render_data)});
};

FilterLocations.prototype.updateLocations = function(data) {
    this.locationWidgetPage.updateLocations(data);
    if (data.prefs.search.auto_select_display_trials_outside_locations) {
        data.prefs.search.display_trials_outside_locations = false;
        data.prefs.search.auto_select_display_trials_outside_locations = false;
        $('#display_trials_outside_locations').prop('checked', false);
    }
    return true;
};

FilterLocations.prototype.removeLocation = function(data, elem) {
    this.locationWidgetPage.removeLocation(data, elem);
    if (data.selected_locations.length == 0 && !data.prefs.search.display_trials_outside_locations) {
        data.prefs.search.display_trials_outside_locations = true;
        data.prefs.search.auto_select_display_trials_outside_locations = true;
        $('#display_trials_outside_locations').prop('checked', 'checked');
    }
    return true;
};

FilterLocations.prototype.updateDisplayTrialsOutsideLocations = function(data, elem) {
    return this.locationWidgetPage.updateDisplayTrialsOutsideLocations(data, elem);
};
