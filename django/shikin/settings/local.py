from .default import *

SECRET_KEY="qaul-k)eiao^o%txhxw+(hz*im+yd+kyto$66qxztkc+$jb-3t"
DEBUG = True
ALLOWED_HOSTS="shikin.localhost"

DATABASES = {
    "default": {
         'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
        },
    }
}


def show_toolbar(request):
    return True


INSTALLED_APPS += ("debug_toolbar",)
MIDDLEWARE += ("debug_toolbar.middleware.DebugToolbarMiddleware",)
DEBUG_TOOLBAR_CONFIG = {"SHOW_TOOLBAR_CALLBACK": show_toolbar}
