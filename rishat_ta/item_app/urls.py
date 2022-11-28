from django.urls import path

from . import views

app_name = 'item_app'

urlpatterns = [
    # Оплата одного предмета
    path('item/<int:item_id>/', views.item, name='item'),
    path(
        'buy/<id>/',
        views.item_checkout_session,
        name='item_checkout_session'
    ),
    # Оплата заказа
    path('order/<int:order_id>/', views.order, name='order'),
    path(
        'buy-order/<id>/',
        views.order_checkout_session,
        name='order_checkout_session'
    ),
    # Странички успешной и неуспешной оплаты
    path('success/', views.PaymentSuccessView.as_view(), name='success'),
    path('failed/', views.PaymentFailedView.as_view(), name='failed'),
]
