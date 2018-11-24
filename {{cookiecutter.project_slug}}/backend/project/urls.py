from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import include, path
from django.views.i18n import JavaScriptCatalog

import debug_toolbar

from main.views import (
    bad_request, page_not_found, permission_denied, server_error,
    simulated_error, change_language,
)

# pylint: disable=invalid-name
urlpatterns = [
    path('admin/', admin.site.urls),
    path('jsi18n/', JavaScriptCatalog.as_view(), name='javascript-catalog'),
    path('simulated-error/', simulated_error),
    path('hijack/', include('hijack.urls')),
    path('change-language/', change_language, name='change-language'),
]

if settings.DEBUG:
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += [
        path('__debug__/', include(debug_toolbar.urls)),
        path('error400/', bad_request),
        path('error403/', permission_denied),
        path('error404/', page_not_found),
        path('error500/', server_error),
    ]

admin.site.site_header = settings.PROJECT_DISPLAY_NAME

# pylint: disable=invalid-name
handler400 = 'main.views.bad_request'
handler403 = 'main.views.permission_denied'
handler404 = 'main.views.page_not_found'
handler500 = 'main.views.server_error'
