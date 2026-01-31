from .base import *

# debug_toolbar settings
if DEBUG:
    INTERNAL_IPS = ("192.168.17.55", "192.168.8.82", "192.168.37.246", "192.168.3.134", "192.168.3.244", "192.168.31.185", "192.168.32.52", "192.168.48.87", "192.168.61.161", "192.168.41.36", '0.0.0.0')
    # MIDDLEWARE += ("debug_toolbar.middleware.DebugToolbarMiddleware",)

    # print(INTERNAL_IPS)
    # this is installed django-debug-toolbar package
    INSTALLED_APPS += ("debug_toolbar",)

    def show_toolbar(request):
        return True
    SHOW_TOOLBAR_CALLBACK = show_toolbar

    # this is toolbar panels that we want to use
    DEBUG_TOOLBAR_PANELS = [
        "debug_toolbar.panels.versions.VersionsPanel",
        "debug_toolbar.panels.timer.TimerPanel",
        "debug_toolbar.panels.settings.SettingsPanel",
        "debug_toolbar.panels.headers.HeadersPanel",
        "debug_toolbar.panels.request.RequestPanel",
        "debug_toolbar.panels.sql.SQLPanel",
        "debug_toolbar.panels.staticfiles.StaticFilesPanel",
        "debug_toolbar.panels.templates.TemplatesPanel",
        "debug_toolbar.panels.cache.CachePanel",
        "debug_toolbar.panels.signals.SignalsPanel",
        "debug_toolbar.panels.logging.LoggingPanel",
        "debug_toolbar.panels.redirects.RedirectsPanel",
    ]

    DEBUG_TOOLBAR_CONFIG = {
        "INTERCEPT_REDIRECTS": False,
    }