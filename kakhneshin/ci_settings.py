from .settings import *

DEBUG = False
DATABASES = {
  'default': {
    'ENGINE': 'django.db.backends.postgresql',
    'NAME': 'kakhneshin',
    'USER': 'kakhneshin',
    'PASSWORD': 'strongpassword',
    'HOST': 'postgres',
    'PORT': '5432',
  }
}

HEADLESS_SELENIUM = True
SELENIUM_SERVER = {'host': 'selenium', 'port': 4444}
