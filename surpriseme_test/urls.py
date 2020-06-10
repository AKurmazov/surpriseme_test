from django.conf.urls import url, include
from django.contrib import admin

urlpatterns = [
    # admin page
    url(r'^admin/', admin.site.urls),

    url(r'^accounts/', include('django.contrib.auth.urls')),
    url('', include('payouts.urls')),
]
