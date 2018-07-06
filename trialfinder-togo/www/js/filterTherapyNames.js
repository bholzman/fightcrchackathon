function FilterTherapyNames() {
    this.name = 'filter-therapy_names';
    this.templatePath = 'filter_therapy_names.html';
}

FilterTherapyNames.prototype = Object.create(Page.prototype);
FilterTherapyNames.prototype.render_data = function (data) {
  var page_render_data = Page.prototype.render_data.call(this, data);

  page_render_data.therapy_names = data.prefs.search.therapy_names;
  page_render_data.prefs = data.prefs;
  page_render_data.filters_selected = '-selected';
  return page_render_data;
};

FilterTherapyNames.prototype.update = function (data, elem) {
  data.prefs.search.therapy_names = $(elem).val();
};

