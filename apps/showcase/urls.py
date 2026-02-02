from django.urls import path
from django.views.generic import TemplateView

app_name = 'showcase'

urlpatterns = [
    # JANGAN pakai '/' di awal path! [web:23]
    path('dkkm-ppmi/', TemplateView.as_view(template_name='showcase/dkkm.html'), name='dkkm'),
    path('saudah-travel/', TemplateView.as_view(template_name='showcase/saudahtravel.html'), name='saudah-travel'),
    path('jastipin/', TemplateView.as_view(template_name='showcase/jastipin.html'), name='jastipin'),
]
