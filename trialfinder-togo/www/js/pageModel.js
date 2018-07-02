function Controller(pages, data) {
    this.pages = pages;
    this.target = $('.app');
    this.data = data;
}

Controller.prototype.initialize = function() {
    if (this.data.prefs.app.onTrialList) {
        if (this.data.prefs.search.search) {
            this.goToPage('trialSearch');
        } else {
            this.goToPage('trialList');
        }
    } else {
        this.pages[0].render(this.target, this.data);
        this.curPage = 0;
    }
};

Controller.prototype.nextPage = function() {
    if (this.curPage < this.pages.length - 1) {
        this.curPage = this.curPage + 1;
    }
    this.pages[this.curPage].render(this.target, this.data);
};

Controller.prototype.prevPage = function() {
    if (this.curPage > 0) {
        this.curPage = this.curPage - 1;
    }
    this.pages[this.curPage].render(this.target, this.data);
};

Controller.prototype.goToPage = function(name) {
    for (i = 0; i < this.pages.length; i++) {
        if (this.pages[i].name === name) {
            this.curPage = i;
            this.data.pageArgs = [].slice.call(arguments, 1);
            this.pages[this.curPage].render(this.target, this.data);
            this.data.prefs.save();
            break;
        }
    }
};

Controller.prototype.pageCall = function(func) {
    var page = this.pages[this.curPage];
    var render_data = page.render_data(this.data);
    var rerender = page[func].apply(page, [render_data].concat([].slice.call(arguments, 1)));

    this.data.prefs.save();

    // re-render as state may have changed
    if (rerender) {
        page.render(this.target, this.data);
    }

};

var Footer;
$.ajax('footer.html').done(function(content) {
    Mustache.parse(content);
    Footer = content;
});

function Page() {
    this.name = undefined;
    this.templatePath = undefined;
    this.template = undefined;
}

Page.prototype.render = function(target, data) {
    if (typeof this.template === "undefined") {
        $.ajax(this.templatePath, {context: this})
         .done(function(content) {
             Mustache.parse(content);
             this.template = content;
             this.render(target, data);
         });
    } else {
        var render_data = this.render_data(data);
        if (typeof Footer !== 'undefined') {
            var footer = Mustache.render(Footer, render_data);
        }
        target.html(Mustache.render(this.template, render_data, {'footer': footer}));

        this.after_render(data);
    }
};

Page.prototype.render_data = function(data) {
    return {'last_update': data.last_update()};
};

Page.prototype.after_render = function(data) { };
