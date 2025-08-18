"""
URL configuration for Arsal's Blog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from tweet.admin import admin_site

urlpatterns = [
    path('admin/', admin_site.urls),  # Custom superuser-only admin
    path('', include('tweet.urls')),  # Main app URLs (includes home, blog, etc.)
    path('accounts/', include('django.contrib.auth.urls')),  # Authentication URLs
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
