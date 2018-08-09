"""icomic URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from comic_strip.views import comic_strip_listing, comic_strip
from comic_strip import urls as urls_comic_strip
from tickets import urls as urls_tickets
from accounts import urls as urls_accounts
from cart import urls as urls_cart
from checkout import urls as urls_checkout
from productivity import urls as urls_productivity
from forum import urls as urls_forum
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
] + static(MEDIA_URL, document_root=MEDIA_ROOT)
