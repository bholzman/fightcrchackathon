function FAQ() {
    this.name = 'faq';
    this.templatePath = 'faq.html';
}

FAQ.prototype = Object.create(Page.prototype);

FAQ.prototype.render_data = function(data) {
    var page_render_data = Page.prototype.render_data.call(this, data);

    page_render_data.faqs = data.faqs;

    page_render_data.faq_selected = '-selected';
    return page_render_data;
};
