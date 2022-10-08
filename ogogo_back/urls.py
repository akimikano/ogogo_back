from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import routers, permissions
from apps.hospital.urls import hospital_router

router = routers.DefaultRouter()
router.registry.extend(hospital_router.registry)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('apps.users.urls')),
    path('api/', include(router.urls)),
]

if settings.DEBUG:
    schema_view = get_schema_view(
        openapi.Info(
            title="Social Network API",
            default_version='v1',
            description="Social Network API",
            terms_of_service="",
            contact=openapi.Contact(email="akim.j.2002@gmail.com"),
        ),
        public=True,
        permission_classes=(permissions.AllowAny,),
    )
    urlpatterns = urlpatterns + [
        path(r'api/swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    ] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) \
      + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)