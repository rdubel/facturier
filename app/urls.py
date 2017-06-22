from django.conf.urls import url, include
from django.views.generic import TemplateView

urlpatterns = [
    url(r'bonjour/^$', TemplateView.as_view(template_name="homepage.html"), name='home'),
]
