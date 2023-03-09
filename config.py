import os


class Config(object):
    CONTACT_EMAIL = os.environ.get("CONTACT_EMAIL", "default")
    CONTACT_PHONE = os.environ.get("CONTACT_PHONE", "default")
    DEPARTMENT_NAME = os.environ.get("DEPARTMENT_NAME", "default")
    DEPARTMENT_URL = os.environ.get("DEPARTMENT_URL", "default")
    RATELIMIT_HEADERS_ENABLED = False
    RATELIMIT_STORAGE_URI = os.environ.get("REDIS_URL", "default")
    SECRET_KEY = os.environ.get("SECRET_KEY", "default")
    SERVICE_NAME = os.environ.get("SERVICE_NAME", "default")
    SERVICE_PHASE = os.environ.get("SERVICE_PHASE", "default")
    SERVICE_URL = os.environ.get("SERVICE_URL", "default")
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SECURE = True
