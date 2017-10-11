function Controller(pages) {
    this.pages = pages;
    this.target = $('.app');
}

Controller.prototype.initialize = function() {
    this.pages[0].render(this.target);
    this.curPage = 0;
};

Controller.prototype.nextPage = function() {
    if (this.curPage < this.pages.length - 1) {
        this.curPage = this.curPage + 1;
    }
    this.pages[this.curPage].render(this.target);
};

Controller.prototype.prevPage = function() {
    if (this.curPage > 0) {
        this.curPage = this.curPage - 1;
    }
    this.pages[this.curPage].render(this.target);
};

Controller.prototype.goToPage = function(name) {
    for (i = 0; i < this.pages.length; i++) {
        if (this.pages[i].name === name) {
            this.curPage = i;
            this.pages[this.curPage].render(this.target);
            break;
        }
    }
};

function Page() {
    this.name = undefined;
    this.templatePath = undefined;
    this.template = undefined;
}

Page.prototype.render = function(target) {
    if (typeof this.template === "undefined") {
        $.ajax(this.templatePath, {context: this})
         .done(function(content) {
             Mustache.parse(content);
             this.template = content;
             this.render(target);
         });
    } else {
        target.html(Mustache.render(this.template));
    }
}
