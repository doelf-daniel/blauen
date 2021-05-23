# -*- coding: utf-8 -*-
"""
Local settings
- Run in Debug mode
- Use console backend for emails
- Add Django Debug Toolbar
- Add django-extensions as app
"""

import os

from .common import *  # noqa



# DEBUG
# ------------------------------------------------------------------------------
DEBUG = True
if 'TEMPLATES' in locals():
    for num, t in enumerate(TEMPLATES):
        if type(t.get('OPTIONS')) is dict:
            TEMPLATES[num]['OPTIONS']['debug'] = DEBUG

# Mail settings
# ------------------------------------------------------------------------------
EMAIL_HOST = 'localhost'
EMAIL_BACKEND = env(
    'DJANGO_EMAIL_BACKEND',
    default='django.core.mail.backends.console.EmailBackend'
)

# CACHING
# ------------------------------------------------------------------------------
CACHES = {
    'default': {
        'BACKEND': 'django.core.cache.backends.locmem.LocMemCache',
        'LOCATION': ''
    }
}

# django-debug-toolbar
# ------------------------------------------------------------------------------
# MIDDLEWARE += ('debug_toolbar.middleware.DebugToolbarMiddleware',)
# INSTALLED_APPS += ('debug_toolbar', )

DEBUG_TOOLBAR_CONFIG = {
    'DISABLE_PANELS': [
        'debug_toolbar.panels.redirects.RedirectsPanel',
    ],
    'SHOW_TEMPLATE_CONTEXT': True,
}

# django-extensions
# ------------------------------------------------------------------------------
INSTALLED_APPS += ('django_extensions',)

# TESTING
# ------------------------------------------------------------------------------
TEST_RUNNER = 'django.test.runner.DiscoverRunner'

# Your local stuff: Below this line define 3rd party library settings
# ------------------------------------------------------------------------------
ALLOWED_HOSTS = env.list('localhost', 'DJANGO_ALLOWED_HOSTS', default=['*'])

# https://docs.djangoproject.com/en/1.7/ref/settings/#databases
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'doelf_blauen',  #
        'USER': 'doelf',
        'PASSWORD': 'rAC9sFBS',
        'HOST': 'localhost',
        'PORT': '33000',  # Set to empty string for default.
    }
}
# ------------- END DATABASE CONFIGURATION -------------
