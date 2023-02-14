from django.urls import include, path

app_name = 'users'

urlpatterns = [
    path('v1/', include('djoser.urls')),
    path('v1/', include('djoser.urls.authtoken')),
]
