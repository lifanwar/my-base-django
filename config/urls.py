from django.contrib import admin
from django.urls import path, include
from apps.core.views import HomeView
from django.conf.urls.i18n import i18n_patterns


urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/', include('django.conf.urls.i18n')),
]

# URLs dengan language prefix (/en/, /id/)
urlpatterns += i18n_patterns(
    path('', HomeView.as_view(), name='home'),
    path('', include('apps.showcase.urls')),
)
