from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('', include('payment.urls', namespace='payment')),
    path('admin/', admin.site.urls),
]
