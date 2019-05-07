function Filters() {
    this.name = 'filters';
    this.templatePath = 'filters.html';
}

Filters.prototype = Object.create(Page.prototype);
Filters.prototype.render_data = function(data) {
    var page_render_data = Page.prototype.render_data.call(this, data);

    var search_prefs = data.prefs.search;

    function tristate(val, t, f, u) {
        return val === true ? (t||'Yes') : val === false ? (f||'No') : (u||'Show all trials');
    }

    page_render_data.filters = [{
        tag: 'locations',
        name: 'Location Preferences',
        value: (search_prefs.locations || []).join(', ')
    }, {
        tag: 'is_immunotherapy_trial',
        name: 'Only Show Immunotherapy Trials',
        value: tristate(search_prefs.is_immunotherapy_trial)
    }, {
        tag: 'prior_io_ok',
        name: 'Show If Prior Immunotherapy Use Is Allowed',
        value: tristate(search_prefs.prior_io_ok, 'Allowed', 'Not allowed')
    }, {
        tag: 'recruitment_statuses',
        name: 'Recruitment Status',
        value: (search_prefs.recruitment_statuses || ['No filters']).join(', ')
    }, {
        tag: 'phases',
        name: 'Phase',
        value: (search_prefs.phases || ['No filters']).join(', ')
    }, {
        tag: 'date_added',
        name: 'Date Added',
        value: search_prefs.date_added || 'No filters'
    }];

    page_render_data.filters_selected = '-selected';
    return page_render_data;
};

Filters.prototype.resetFilters = function(data) {
  if (confirm("Are you sure you want to reset all filters?")) {
    controller.data.prefs.clearSearch();
    controller.data.prefs.save();
    controller.goToPage('msStatusQuestion');
  }
};
