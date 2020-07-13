from .default import *

DEBUG = True

ALLOWED_HOSTS += ["127.0.0.1"]


def show_toolbar(request):
    return True


INSTALLED_APPS += ("debug_toolbar",)
MIDDLEWARE += ("debug_toolbar.middleware.DebugToolbarMiddleware",)
DEBUG_TOOLBAR_CONFIG = {"SHOW_TOOLBAR_CALLBACK": show_toolbar}
