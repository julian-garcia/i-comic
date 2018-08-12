"""icomic URL Configuration
The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
"""
from django.contrib import admin
from django.urls import path, include
from comic_strip.views import comic_strip_listing
from comic_strip import urls as urls_comic_strip
from tickets import urls as urls_tickets
from accounts import urls as urls_accounts
from cart import urls as urls_cart
from checkout import urls as urls_checkout
from productivity import urls as urls_productivity
from forum import urls as urls_forum
from documentation import urls as urls_documentation
from django.conf.urls.static import static
from .settings import MEDIA_URL, MEDIA_ROOT

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', comic_strip_listing, name='index'),
    path('comic-strip/', include(urls_comic_strip)),
    path('tickets/', include(urls_tickets)),
    path('account/', include(urls_accounts)),
    path('cart/', include(urls_cart)),
    path('checkout/', include(urls_checkout)),
    path('productivity/', include(urls_productivity)),
    path('forum/', include(urls_forum)),
    path('doc/', include(urls_documentation)),
] + static(MEDIA_URL, document_root=MEDIA_ROOT)
