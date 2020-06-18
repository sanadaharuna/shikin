from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

from . import settings

urlpatterns = [
    path("", TemplateView.as_view(template_name="frontpage.html"), name="frontpage"),
    path("kanri", TemplateView.as_view(template_name="kanri.html"), name="kanri"),
    path("erad/", include("erad.urls")),
    path("grant/", include("grant.urls")),
    path("kanrisite/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
