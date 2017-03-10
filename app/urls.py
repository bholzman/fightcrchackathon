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
    url(r'^db', fightcrctrials.views.db, name='db'),
    url(r'^trials/', fightcrctrials.views.index, name='trials'),
    url(r'^send-trial-closed-email/', fightcrctrials.views.send_trial_closed_email),
    url(r'^favicon.ico', RedirectView.as_view(url='/static/favicon.ico')),
    url(r'^faq/', fightcrctrials.views.faq, name='faq'),
    url(r'^contact-us/', fightcrctrials.views.contactus, name='contact_us'),
    url(r'^admin/', include(admin.site.urls))
]
