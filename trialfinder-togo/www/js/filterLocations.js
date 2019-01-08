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
    return this.locationWidgetPage.updateLocations(data);
};

FilterLocations.prototype.removeLocation = function(data, elem) {
    return this.locationWidgetPage.removeLocation(data, elem);
};

FilterLocations.prototype.updateDisplayTrialsOutsideLocations = function(data, elem) {
    return this.locationWidgetPage.updateDisplayTrialsOutsideLocations(data, elem);
};
