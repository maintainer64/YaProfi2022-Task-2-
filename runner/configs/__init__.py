try:
    from .local import ConfigApp
except ImportError:
    from .base import ConfigApp

config = ConfigApp()
