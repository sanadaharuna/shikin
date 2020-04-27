from django.contrib import admin
from django.urls import include, path
from django.views.generic import TemplateView

# from grant.views import ShikinAdminView

from . import settings

urlpatterns = [
    path("", TemplateView.as_view(template_name="frontpage.html"), name="frontpage"),
    # path("shikin_admin", ShikinAdminView.as_view(), name="shikin_admin"),
    path("erad/", include("erad.urls")),
    path("grant/", include("grant.urls")),
    path("shikin_admin/", admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
]

if settings.DEBUG:
    import debug_toolbar

    urlpatterns += [path("__debug__/", include(debug_toolbar.urls))]
