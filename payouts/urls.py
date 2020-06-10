from django.conf.urls import url
from payouts.views import home

urlpatterns = [
    url('', home, name="home")
]
