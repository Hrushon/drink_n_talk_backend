from django.urls import include, path
# from rest_framework import routers

app_name = 'users'

urlpatterns = [
    path('auth/', include('djoser.urls.authtoken')),
]
