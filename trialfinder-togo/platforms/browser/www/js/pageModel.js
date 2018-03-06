function Controller(pages, data) {
    this.pages = pages;
    this.target = $('.app');
    this.data = data;
}

Controller.prototype.initialize = function() {
    this.pages[0].render(this.target, this.data);
    this.curPage = 0;
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
            break;
        }
    }
};

Controller.prototype.pageCall = function(func) {
    var page = this.pages[this.curPage];
    var render_data = page.render_data(this.data);
    var rerender = page[func].apply(page, [render_data].concat([].slice.call(arguments, 1)));

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
        if (typeof Footer !== 'undefined') {
            var footer = Mustache.render(Footer, this.render_data(data));
        }
        target.html(Mustache.render(this.template, this.render_data(data), {'footer': footer}));
    }
};

Page.prototype.render_data = function(data) {
    return {'last_update': data.last_update()};
};
