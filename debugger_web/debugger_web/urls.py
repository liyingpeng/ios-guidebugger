from django.conf.urls import include, url
from django.contrib import admin
from views import adddata, showdata, buildView, statusChange

urlpatterns = [
    # Examples:
    # url(r'^$', 'debugger_web.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^adddata$', adddata, name='adddata'),
    url(r'^showdata$', showdata, name='showdata'),
    url(r'^buildView$', buildView, name='buildView'),
    url(r'^statusChange$', statusChange, name='statusChange'),
]
