function ImmunoTherapy() {
  this.name = 'immunoTherapy';
  this.templatePath = 'immunoTherapyQuestion.html';
}


ImmunoTherapy.prototype = Object.create(Page.prototype);
ImmunoTherapy.prototype.render_data = function(data) {
  var page_render_data = Page.prototype.render_data.call(this, data);
  page_render_data.step = data.prefs.app.wizard;
  page_render_data.data = data;
  return page_render_data;
};

ImmunoTherapy.prototype.onQuestionSubmit = function(data, answer) {
  data.data.prefs.search.hasImmunoTherapy = answer;
  controller.goToPage('trialList');
};
