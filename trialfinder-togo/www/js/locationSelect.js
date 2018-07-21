function LocationSelect() {
    this.name = 'locationSelect';
    this.templatePath = 'location_select.html';
    this.locationWidgetPage = new LocationWidget();
    var that = this;
    $.ajax(this.locationWidgetPage.templatePath).done(function (content) {
        Mustache.parse(content);
        that.locationWidget = content;
    });
}

LocationSelect.prototype = Object.create(Page.prototype);
LocationSelect.prototype.render_data = function(data) {
    var page_render_data = Page.prototype.render_data.call(this, data);
    page_render_data = Object.assign(page_render_data, this.locationWidgetPage.render_data(data));
    page_render_data.matching_trials = Search(data.trials, data.prefs.search).length;
    return page_render_data;
};

LocationSelect.prototype.dependencies = function(render_data) {
    return Object.assign(Page.prototype.dependencies.call(this, render_data),
        {locationWidget: Mustache.render(this.locationWidget, render_data)});
};

LocationSelect.prototype.updateLocations = function(data) {
    return this.locationWidgetPage.updateLocations(data);
};

LocationSelect.prototype.updateDisplayTrialsOutsideLocations = function(data, elem) {
    this.locationWidgetPage.updateDisplayTrialsOutsideLocations(data, elem);
    return true;
};
