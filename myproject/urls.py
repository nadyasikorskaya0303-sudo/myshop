from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap
from shopapp.sitemaps import ShopSitemap

sitemaps = {
    'shop': ShopSitemap,
}

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('shopapp.urls')),
    path('accounts/', include('myauth.urls')),
    path('blog/', include('blogapp.urls')),
    path('sitemap.xml', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap'),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
