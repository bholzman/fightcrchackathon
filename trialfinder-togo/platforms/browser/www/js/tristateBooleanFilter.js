function TristateBooleanFilter() {
  // this is actually an abstract class
  // subclasses have to set field and then call this constructor
  this.name = 'filter-' + this.field;
  this.templatePath = 'filter_' + this.field + '.html';
}

TristateBooleanFilter.prototype = Object.create(Page.prototype);
TristateBooleanFilter.prototype.render_data = function(data) {
    var page_render_data = Page.prototype.render_data.call(this, data);

    var field = this.field;
    var set_selected = function (comp) {
        return data.prefs.search[field] === comp ? 'selected' : '';
    };

    page_render_data.true_selected = set_selected(true);
    page_render_data.false_selected = set_selected(false);
    page_render_data.none_selected = set_selected(undefined);

    page_render_data.prefs = data.prefs;

    page_render_data.filters_selected = '-selected';

    return page_render_data;
};

var tristate = {
    true: true,
    false: false,
    undefined: undefined
};

TristateBooleanFilter.prototype.update = function(data, elem) {
    var $all_buttons = $('button[name=' + this.field + ']');
    var $elem = $(elem);
    $all_buttons.removeClass('selected');
    $elem.addClass('selected');
    data.prefs.search[this.field] = tristate[$elem.prop('value')];
    return true;
};
