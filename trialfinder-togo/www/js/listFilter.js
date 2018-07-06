function ListFilter() {
    // this is actually an abstract class
    // subclasses have to set field and then call this constructor
    this.name = 'filter-' + this.field
    this.templatePath = 'filter_' + this.field + '.html';
    // subclasses can also set "trial_field" if it is different (or even a "trial_fields" array)
}

ListFilter.prototype = Object.create(Page.prototype);
ListFilter.prototype.render_data = function(data) {
    var page_render_data = Page.prototype.render_data.call(this, data);

    var selected_values = data.prefs.search[this.field] || [];

    var trial_fields = this.trial_fields || [this.trial_field || this.field];

    var values = {};
    data.trials.forEach(function (trial) {
        trial_fields.forEach(function (trial_field) {
            if (!(trial[trial_field] in values)) {
                values[trial[trial_field]] = {
                    value: trial[trial_field],
                    selected: selected_values.includes(trial[trial_field]) ? 'selected' : ''
                };
            }
        });
    });
    page_render_data[this.field] = Object.values(values).sort(
        function (a, b) { return a.value < b.value ? -1 : a.value > b.value ? 1 : 0; }
    );

    page_render_data.prefs = data.prefs;

    page_render_data.filters_selected = '-selected';

    return page_render_data;
};

ListFilter.prototype.update = function(data, elem) {
    $(elem).toggleClass('selected');
    var $selectedButtons = $('button[name=' + this.field + '].selected');
    if ($selectedButtons.length > 0) {
        data.prefs.search[this.field] = $selectedButtons.map(function() { return this.value }).get();
    } else {
        data.prefs.search[this.field] = undefined;
    }
    return true;
};
