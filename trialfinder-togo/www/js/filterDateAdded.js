function FilterDateAdded() {
    this.name = 'filter-date_added';
    this.templatePath = 'filter_date_added.html';
}

FilterDateAdded.prototype = Object.create(Page.prototype);
FilterDateAdded.prototype.render_data = function(data) {
    var page_render_data = Page.prototype.render_data.call(this, data);
    page_render_data.date_added = data.prefs.search.date_added;
    page_render_data.prefs = data.prefs;
    page_render_data.filters_selected = '-selected';
    return page_render_data;
};

FilterDateAdded.prototype.update = function(data, elem) {
    data.prefs.search.date_added = $(elem).val();
    return true;
};

FilterDateAdded.prototype.clear = function(data) {
    data.prefs.search.date_added = undefined;
    return true;
};
