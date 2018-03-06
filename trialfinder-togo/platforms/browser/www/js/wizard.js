function Wizard() {
    this.name = 'wizard';
    this.templatePath = 'wizard.html';
}



Wizard.prototype = Object.create(Page.prototype);
Wizard.prototype.render_data = function(data) {
    var page_render_data = Page.prototype.render_data.call(this, data);
    page_render_data.step = data.prefs.app.wizard;
    return page_render_data;
};
