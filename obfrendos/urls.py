from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView


from obfrendos import settings



urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name='index.html'), name='home'),
    path('users/', include('users.urls')),
    path('communication/', include('communication.urls')),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_URL)

# Добавление URL-шаблона для медиафайлов только в режиме отладки
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)