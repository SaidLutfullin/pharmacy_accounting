from django.contrib import admin
from django.urls import path, include
from django.conf.urls import handler403

urlpatterns = [
    path('__debug__/', include('debug_toolbar.urls')),
    path('admin/', admin.site.urls),
    path('', include('src.common.urls')),
    path('', include('src.profiles.urls')),
    path('', include('src.drugs.urls')),
]

handler403 = 'src.common.views.forbidden_page_view'
