from ytbmp3.settings.base import *


INSTALLED_APPS += ('debug_toolbar',)

MIDDLEWARE_CLASSES += ('debug_toolbar.middleware.DebugToolbarMiddleware', )

# The Django Debug Toolbar will only be shown to these client IPs.
INTERNAL_IPS = (
    '127.0.0.1',
)
ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
SRC_PATH = os.path.join(ROOT_PATH, 'src')
CONF_PATH = os.path.join(ROOT_PATH, 'conf')
DEBUG_TOOLBAR_CONFIG = {
    'INTERCEPT_REDIRECTS': False,
    'SHOW_TEMPLATE_CONTEXT': True,
    'HIDE_DJANGO_SQL': False,
}
