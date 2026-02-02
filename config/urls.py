from django.contrib import admin
from django.urls import path, include
from apps.core.views import HomeView

urlpatterns = [
    path('admin/', admin.site.urls),

    path('', HomeView.as_view(), name='home'),
    path('projects/', include('apps.showcase.urls')),
]
