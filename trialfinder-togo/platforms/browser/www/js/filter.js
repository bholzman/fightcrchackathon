function Filter() {
    this.name = 'filter';
    this.templatePath = 'filter.html';
}

Filter.prototype = Object.create(Page.prototype);
Filter.prototype.render_data = function(data) {
debugger
    var page_render_data = Page.prototype.render_data.call(this, data);

    page_render_data.filters_selected = '-selected';
    return page_render_data;
};
