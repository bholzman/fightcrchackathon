function ImmunoTherapyPreviouslyUsed() {
  this.name = 'immunoTherapyPreviouslyUsed';
  this.templatePath = 'immunoTherapyPreviouslyUsedQuestion.html';
}


ImmunoTherapyPreviouslyUsed.prototype = Object.create(Page.prototype);
ImmunoTherapyPreviouslyUsed.prototype.render_data = function(data) {
  var page_render_data = Page.prototype.render_data.call(this, data);
  page_render_data.step = data.prefs.app.wizard;
  page_render_data.data = data;
  return page_render_data;
};

ImmunoTherapyPreviouslyUsed.prototype.onQuestionSubmit = function(data, answer) {
  data.data.prefs.search.hasPreviouslyUsedImmunoTherapy = answer;
  controller.goToPage('locationSelect');
};
