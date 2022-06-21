from django.conf.urls import include
from django.urls import re_path
from wagtail.core import urls as wagtail_urls

urlpatterns = []

urlpatterns += [re_path(r"^", include(wagtail_urls))]
