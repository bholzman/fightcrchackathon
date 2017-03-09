from django.conf.urls import include, url

from django.contrib import admin
admin.autodiscover()

import fightcrctrials.views

# Examples:
# url(r'^$', 'app.views.home', name='home'),
# url(r'^blog/', include('blog.urls')),

urlpatterns = [
    url(r'^$', fightcrctrials.views.index, name='index'),
    url(r'^db', fightcrctrials.views.db, name='db'),
    url(r'^admin/', include(admin.site.urls)),
]
