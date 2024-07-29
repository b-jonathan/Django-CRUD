#!C:/Users/user/AppData/Local/Programs/Python/Python310/python.exe
from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('qc.urls')),
    path('admin/', admin.site.urls),
]
