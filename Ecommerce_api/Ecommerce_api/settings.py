from pathlib import Path
import os
from datetime import timedelta

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# ---------------------------------------------------------------------
# SECURITY SETTINGS
# ---------------------------------------------------------------------

# SECURITY WARNING: keep the secret key used in production secret!
# Use environment variables or a separate configuration file for production
SECRET_KEY = os.getenv("SECRET_KEY", "django-insecure-your-default-secret-key")

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True  # Set DEBUG=False in production

# Define the allowed hosts; update this with your domain for deployment
ALLOWED_HOSTS = ["your-username.pythonanywhere.com", "127.0.0.1", "localhost"]

# ---------------------------------------------------------------------
# APPLICATION DEFINITION
# ---------------------------------------------------------------------

INSTALLED_APPS = [
    # Default Django apps
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    # Third-party apps
    "rest_framework",  # Django REST Framework for building APIs
    "django_filters",  # Provides advanced filtering capabilities
    "rest_framework_simplejwt",  # JWT authentication support
    "rest_framework.authtoken",  # Token authentication (if needed)
    # Your apps
    "product",  # Your custom app for product management
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",  # Security enhancements
    "django.contrib.sessions.middleware.SessionMiddleware",  # Manages sessions across requests
    "django.middleware.common.CommonMiddleware",  # Common HTTP middleware
    "django.middleware.csrf.CsrfViewMiddleware",  # Protects against CSRF attacks
    "django.contrib.auth.middleware.AuthenticationMiddleware",  # Associates users with requests
    "django.contrib.messages.middleware.MessageMiddleware",  # Enables messaging framework
    "django.middleware.clickjacking.XFrameOptionsMiddleware",  # Prevents clickjacking
]

ROOT_URLCONF = "Ecommerce_api.urls"  # Points to the root URL configuration

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],  # Directories where Django looks for template files
        "APP_DIRS": True,  # Includes templates from installed apps
        "OPTIONS": {
            "context_processors": [  # Injects variables into all templates
                "django.template.context_processors.debug",
                "django.template.context_processors.request",  # Adds 'request' variable
                "django.contrib.auth.context_processors.auth",  # Adds 'user' and 'perms'
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "Ecommerce_api.wsgi.application"  # WSGI application entry point

# ---------------------------------------------------------------------
# DATABASE CONFIGURATION
# ---------------------------------------------------------------------

# Using SQLite for simplicity; suitable for development and small deployments
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",  # Database engine for PostgreSQL
        "NAME": "therx",                           # Name of your PostgreSQL database
        "USER": "postgres",                         # Your PostgreSQL username
        "PASSWORD": "karimtz999",                  # Your PostgreSQL password
        "HOST": "localhost",                        # Use 'localhost' or '127.0.0.1'
        "PORT": "5433",                            # The port your PostgreSQL server is running on
    }
}

# ---------------------------------------------------------------------
# PASSWORD VALIDATION
# ---------------------------------------------------------------------

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",  # Checks for similarity with user attributes
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",  # Enforces minimum length
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",  # Prevents common passwords
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",  # Disallows fully numeric passwords
    },
]

# ---------------------------------------------------------------------
# INTERNATIONALIZATION
# ---------------------------------------------------------------------

LANGUAGE_CODE = "en-us"  # Language code for this installation
TIME_ZONE = "UTC"  # Time zone
USE_I18N = True  # Enables Django’s translation system
USE_L10N = True  # Enables localized formatting
USE_TZ = True  # Enables timezone-aware datetimes

# ---------------------------------------------------------------------
# STATIC AND MEDIA FILES
# ---------------------------------------------------------------------

# Static files (CSS, JavaScript, Images)
STATIC_URL = "/static/"  # URL to access static files
STATIC_ROOT = os.path.join(
    BASE_DIR, "static"
)  # Directory where static files are collected

# Media files (User-uploaded content)
MEDIA_URL = "/media/"  # URL to access media files
MEDIA_ROOT = os.path.join(BASE_DIR, "media")  # Directory to store uploaded media files

# ---------------------------------------------------------------------
# DJANGO REST FRAMEWORK CONFIGURATION
# ---------------------------------------------------------------------

REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework_simplejwt.authentication.JWTAuthentication",  # Use JWT authentication
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",  # Enable pagination
    "PAGE_SIZE": 10,  # Default number of items per page
}

# ---------------------------------------------------------------------
# JWT SETTINGS
# ---------------------------------------------------------------------

SIMPLE_JWT = {
    "ACCESS_TOKEN_LIFETIME": timedelta(days=7),  # Access token lifespan
    "REFRESH_TOKEN_LIFETIME": timedelta(days=7),  # Refresh token lifespan
    # Add other settings as needed
}
# ---------------------------------------------------------------------
# SECURITY SETTINGS FOR PRODUCTION
# ---------------------------------------------------------------------

# all this settings for befor deployment
# SECURE_HSTS_SECONDS = 3600                      # Enforce HTTPS for one hour
# SECURE_HSTS_INCLUDE_SUBDOMAINS = True           # Apply HSTS to all subdomains
# SECURE_HSTS_PRELOAD = True                      # Allows browsers to preload HSTS
# SECURE_SSL_REDIRECT = True                      # Redirect all HTTP traffic to HTTPS

# CSRF_COOKIE_SECURE = True                       # Use secure cookies for CSRF protection
# SESSION_COOKIE_SECURE = True                    # Use secure cookies for sessions
# X_FRAME_OPTIONS = 'DENY'                        # Protect against clickjacking

# ---------------------------------------------------------------------
# DEFAULT PRIMARY KEY FIELD TYPE
# ---------------------------------------------------------------------

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"  # Default primary key field type

# ---------------------------------------------------------------------
# ADDITIONAL CONFIGURATIONS (IF ANY)
# ---------------------------------------------------------------------

# Add any additional settings or third-party configurations below

# ---------------------------------------------------------------------
# NOTE
# ---------------------------------------------------------------------

# **Note:** Ensure that you replace `'your-username.pythonanywhere.com'` in the `ALLOWED_HOSTS` with your actual PythonAnywhere domain.
# For production, it's highly recommended to:
# - Set `DEBUG = False` to prevent detailed error pages from being displayed to users.
# - Use environment variables or a separate configuration file to manage sensitive information like `SECRET_KEY` and database credentials.
# - Regularly update your dependencies and Django version to include security patches and improvements.
