import stripe
from django.conf import settings
from django.http.response import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.urls import reverse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from .models import Item, Order, Order_items, Tax


def item(request, item_id):
    """Рендер страницы оплаты одного предмета."""
    item = get_object_or_404(Item, pk=item_id)

    return render(
        request,
        'item_app/item.html',
        {
            'item': item,
            'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY
        }
    )


@csrf_exempt
def item_checkout_session(request, id):
    """Stripe-сессия оплаты одного предмета."""
    item = get_object_or_404(Item, pk=id)
    stripe.api_key = settings.STRIPE_SECRET_KEY

    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': 'usd',
                    'product_data': {'name': item.name},
                    'unit_amount': int(item.price * 100),
                },
                'quantity': 1,
            }
        ],
        mode='payment',
        success_url=request.build_absolute_uri(reverse('item_app:success')),
        cancel_url=request.build_absolute_uri(reverse('item_app:failed')),
    )

    return JsonResponse({'sessionId': checkout_session.id})


def order(request, order_id):
    """Рендер страницы оплаты заказа."""
    order = get_object_or_404(Order, pk=order_id)
    items = Order_items.objects.filter(
        order=order).select_related('order', 'item')
    price_sum = sum([item.item_amount * item.item.price for item in items])

    discount_total, tax_total = 0, 0
    if order.discount_amount:
        discount_total = (
            round((price_sum * order.discount_amount.discount_amount / 100), 2)
        )
    if order.tax_amount:
        tax_total = (
            round(
                ((price_sum - discount_total)
                 * order.tax_amount.tax_amount / 100), 2
            )
        )
    total = round((price_sum - discount_total + tax_total), 2)

    return render(
        request,
        'item_app/order.html',
        {
            'items': items,
            'order': order,
            'price_sum': price_sum,
            'discount_total': discount_total,
            'tax_total': tax_total,
            'total': total,
            'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY
        }
    )


def coupon_get_or_create(order):
    """Получение или создание stripe-купона для применения скидки."""
    coupon = {}
    if order.discount_amount:
        try:
            stripe.Coupon.create(
                id=order.discount_amount.pk,
                percent_off=order.discount_amount.discount_amount,
                duration='forever'
            )
        except Exception:
            pass
        coupon = {'coupon': order.discount_amount.pk, }
    return coupon


def tax_get_or_create(order):
    """Получение или создание stripe-налоговой ставки для оплаты налога."""
    tax_rate_id = []
    if order.tax_amount and not order.tax_amount.stripe_tax_rate_id:
        tax_rate = stripe.TaxRate.create(
            display_name=order.tax_amount.tax_name,
            inclusive=False,
            percentage=order.tax_amount.tax_amount
        )
        tax_rate_id = [tax_rate['id']]
        Tax.objects.filter(pk=order.tax_amount.pk).update(
            stripe_tax_rate_id=tax_rate['id'])
    if order.tax_amount and order.tax_amount.stripe_tax_rate_id:
        tax_rate_id = [order.tax_amount.stripe_tax_rate_id]
    return tax_rate_id


@csrf_exempt
def order_checkout_session(request, id):
    """Stripe-сессия для оплаты заказа."""
    order = get_object_or_404(Order, pk=id)
    items = Order_items.objects.filter(
        order=order).select_related('order', 'item')
    price_sum = sum([item.item_amount * item.item.price for item in items])
    stripe.api_key = settings.STRIPE_SECRET_KEY
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': 'usd',
                    'product_data': {'name': order},
                    'unit_amount': (
                        int(price_sum * 100)
                    ),
                },
                'quantity': 1,
                'tax_rates': tax_get_or_create(order),
            }
        ],
        mode='payment',
        discounts=[coupon_get_or_create(order)],
        success_url=request.build_absolute_uri(reverse('item_app:success')),
        cancel_url=request.build_absolute_uri(reverse('item_app:failed')),
    )

    return JsonResponse({'sessionId': checkout_session.id})


class PaymentSuccessView(TemplateView):
    template_name = "item_app/success.html"


class PaymentFailedView(TemplateView):
    template_name = "item_app/failed.html"
