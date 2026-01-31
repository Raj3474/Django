from .base import *

# debug_toolbar settings
if DEBUG:
    INTERNAL_IPS = "ide-cdd34c72ea7f4eb49761c5c2c9921d91-8080.cs50.ws"
    MIDDLEWARE += ("debug_toolbar.middleware.DebugToolbarMiddleware",)

    
    # this is installed django-debug-toolbar package
    INSTALLED_APPS += ("debug_toolbar",)

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