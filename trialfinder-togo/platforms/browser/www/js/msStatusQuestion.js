function MsStatus() {
  this.name = 'msStatusQuestion';
  this.templatePath = 'msStatusQuestion.html';
}



MsStatus.prototype = Object.create(Page.prototype);
MsStatus.prototype.render_data = function(data) {
  var page_render_data = Page.prototype.render_data.call(this, data);
  page_render_data.step = data.prefs.app.wizard;
  page_render_data.data = data;
  return page_render_data;
};

MsStatus.prototype.onQuestionSubmit = function(data, answer) {
  data.data.prefs.search.doesKnowMsStatus = answer;
  controller.goToPage('immunoTherapy');
};
