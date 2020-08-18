try:
    from .local_settings import *
except ImportError:
    from .default import *
