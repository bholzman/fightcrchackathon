function Favorites() {
    this.name = 'favorites';
    this.templatePath = 'trial_list.html';
}

Favorites.prototype = Object.create(TrialList.prototype);
Favorites.prototype.trials = function(data) {
    return data.trials.filter(function (trial) { return trial.favorite });
};

Favorites.prototype.render_data = function(data) {
    var page_render_data = TrialList.prototype.render_data.call(this, data);
    page_render_data.home_selected = '';
    page_render_data.search_selected = '';
    page_render_data.star_selected = '-selected';
    page_render_data.prefs = data.prefs;
    return page_render_data;
};
