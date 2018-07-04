function FilterRecruitmentStatus() {
    this.field = 'recruitment_statuses';
    this.trial_field = 'program_status';
    ListFilter.call(this);
}

FilterRecruitmentStatus.prototype = Object.create(ListFilter.prototype);
