from django.conf.urls import url, include
from django.contrib import admin
from django.views.generic import TemplateView

from app.views import *

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^accounts/', include('allauth.urls')),
    url(r'^proposal/', include('app.urls')),
    url(r'^$', TemplateView.as_view(template_name="homepage.html"), name='home'),
]
