from django.contrib import admin
from django.urls import include, path, re_path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api/', include('users.urls')),
]

schema_view = get_schema_view(
    openapi.Info(
        title="Drink&Talk API",
        default_version='v1',
        description="Документация для проекта D&T",
        # terms_of_service="URL страницы с пользовательским соглашением",
        contact=openapi.Contact(email="i@steblyan.ru"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns += [
    re_path(r'^redoc/$', schema_view.with_ui('redoc', cache_timeout=0),
        name='schema-redoc'),
]
