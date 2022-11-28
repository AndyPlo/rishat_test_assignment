from django.shortcuts import render, get_object_or_404
from .models import Item, Order, Item_order
import stripe
from django.conf import settings
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.urls import reverse


def order(request, order_id):
    order = get_object_or_404(Order, pk=order_id)
    items = Item_order.objects.filter(order=order)
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
        'payment/order.html',
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


def item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)

    return render(
        request,
        'payment/item.html',
        {
            'item': item,
            'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY
        }
    )


@csrf_exempt
def item_checkout_session(request, id):
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
        success_url=request.build_absolute_uri(reverse('payment:success')),
        cancel_url=request.build_absolute_uri(reverse('payment:failed')),
    )

    return JsonResponse({'sessionId': checkout_session.id})


def coupon_create(order):
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
    else:
        coupon = {}
    return coupon


def tax_create(order):
    tax_rate_id = []
    if order.tax_amount:
        tax_rate = stripe.TaxRate.create(
            display_name=order.tax_amount.tax_name,
            inclusive=False,
            percentage=order.tax_amount.tax_amount
        )
        tax_rate_id = [tax_rate['id']]
    return tax_rate_id


@csrf_exempt
def order_checkout_session(request, id):
    order = get_object_or_404(Order, pk=id)
    items = Item_order.objects.filter(order=order)
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
                'tax_rates': tax_create(order),
            }
        ],
        mode='payment',
        discounts=[coupon_create(order)],
        success_url=request.build_absolute_uri(reverse('payment:success')),
        cancel_url=request.build_absolute_uri(reverse('payment:failed')),
    )

    return JsonResponse({'sessionId': checkout_session.id})


class PaymentSuccessView(TemplateView):
    template_name = "payment/success.html"


class PaymentFailedView(TemplateView):
    template_name = "payment/failed.html"
