from django.urls import path
from . import views

app_name = 'payment'

urlpatterns = [
    path('item/<int:item_id>/', views.item, name='item'),
    path('order/<int:order_id>/', views.order, name='order'),
    path(
        'buy/<id>/',
        views.item_checkout_session,
        name='item_checkout_session'
    ),
    path(
        'buy-order/<id>/',
        views.order_checkout_session,
        name='order_checkout_session'
    ),
    path('success/', views.PaymentSuccessView.as_view(), name='success'),
    path('failed/', views.PaymentFailedView.as_view(), name='failed'),
]
