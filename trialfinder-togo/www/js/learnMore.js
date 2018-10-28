function LearnMore() {
  this.name = 'learnMore';
  this.templatePath = 'learn_more.html';
}



LearnMore.prototype = Object.create(Page.prototype);
LearnMore.prototype.render_data = function(data) {
  var page_render_data = Page.prototype.render_data.call(this, data);
  page_render_data.content = $.ajax({
    type: "GET",
    url: data.pageArgs[0] + '.more.html',
    async: false}).responseText;
  page_render_data.data = data;
  return page_render_data;
};
