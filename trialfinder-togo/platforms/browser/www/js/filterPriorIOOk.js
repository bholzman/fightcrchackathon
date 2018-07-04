function FilterPriorIOOk() {
    this.field = 'prior_io_ok';
    TristateBooleanFilter.call(this);
}

FilterPriorIOOk.prototype = Object.create(TristateBooleanFilter.prototype);
