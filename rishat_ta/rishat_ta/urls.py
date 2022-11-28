from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('', include('item_app.urls', namespace='item_app')),
    path('admin/', admin.site.urls),
]
