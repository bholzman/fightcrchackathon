function FilterPhase() {
    this.field = 'phases';
    this.trial_field = 'phase';
    ListFilter.call(this);
}

FilterPhase.prototype = Object.create(ListFilter.prototype);
