function TrialSearch() {
    this.name = 'trialSearch';
    this.templatePath = 'trial_list.html';
}

TrialSearch.prototype = Object.create(TrialList.prototype);
TrialSearch.prototype.render_data = function(data) {
    var page_render_data = TrialList.prototype.render_data.call(this, data);
    page_render_data.inSearch = true;
    page_render_data.search = data.prefs.search.search;
    page_render_data.home_selected = '';
    page_render_data.search_selected = '-selected';
    page_render_data.prefs = data.prefs;
    return page_render_data;
};

TrialSearch.prototype.searchChanged = function(data, event) {
    if (event.keyCode === 13) {
        return controller.goToPage('trialList');
    }
    var search = $('#search').val();
    if (search !== data.prefs.search.search) {
        data.prefs.search.search = search;
        return true;
    } else {
        return false;
    }
};

TrialSearch.prototype.after_render = function(data) {
    TrialList.prototype.after_render(data);
    var $search = $('#search');
    var searchLen = $search.val().length;
    $search[0].selectionStart = searchLen;
    $search[0].selectionEnd = searchLen;
    $search.focus();
};
