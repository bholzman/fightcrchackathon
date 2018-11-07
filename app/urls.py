from django.conf.urls import include, url
from django.contrib import admin
from django.views.generic import RedirectView

admin.autodiscover()

import fightcrctrials.views

# Examples:
# url(r'^$', 'app.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', fightcrctrials.views.welcome, name='welcome'),
    url(r'^trials/', fightcrctrials.views.index, name='trials'),
    url(r'^trials-json/', fightcrctrials.views.index_json, name='trials_json'),
    url(r'^send-trial-closed-email/', fightcrctrials.views.send_trial_closed_email),
    url(r'^favicon.ico', RedirectView.as_view(url='/static/favicon.ico')),
    url(r'^faq/', fightcrctrials.views.faq, name='faq'),
    url(r'^faq-json/', fightcrctrials.views.faq_json, name='faq_json'),
    url(r'^mobile-faq/', fightcrctrials.views.mobile_faq, name='mobile_faq'),
    url(r'^mobile-faq-json/', fightcrctrials.views.mobile_faq_json, name='mobile_faq_json'),
    url(r'^contact-us/', fightcrctrials.views.contactus, name='contact_us'),
    url(r'^admin/', include(admin.site.urls))
]

admin.site.site_header = 'FightCRC Trial Finder administration'
