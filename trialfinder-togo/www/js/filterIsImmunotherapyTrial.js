function FilterIsImmunotherapyTrial() {
    this.field = 'is_immunotherapy_trial';
    TristateBooleanFilter.call(this);
}

FilterIsImmunotherapyTrial.prototype = Object.create(TristateBooleanFilter.prototype);
