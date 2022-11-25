from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path('item/<int:item_id>/', views.item, name='item'),
    path('buy/<id>/', views.create_checkout_session, name='checkout_session'),
    path('success/', views.PaymentSuccessView.as_view(), name='success'),
    path('failed/', views.PaymentFailedView.as_view(), name='failed'),
]
