from django.shortcuts import render, get_object_or_404
from .models import Item
import stripe
from django.conf import settings
from django.http.response import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView
from django.urls import reverse


def item(request, item_id):
    item = get_object_or_404(Item, pk=item_id)

    return render(
        request,
        'payment/index.html',
        {
            'item': item,
            'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY
        }
    )


@csrf_exempt
def create_checkout_session(request, id):
    product = get_object_or_404(Item, pk=id)
    stripe.api_key = settings.STRIPE_SECRET_KEY
    checkout_session = stripe.checkout.Session.create(
        payment_method_types=['card'],
        line_items=[
            {
                'price_data': {
                    'currency': 'usd',
                    'product_data': {'name': product.name},
                    'unit_amount': int(product.price * 100),
                },
                'quantity': 1,
            }
        ],
        mode='payment',
        success_url=request.build_absolute_uri(reverse('payment:success')),
        cancel_url=request.build_absolute_uri(reverse('payment:failed')),
    )

    return JsonResponse({'sessionId': checkout_session.id})


class PaymentSuccessView(TemplateView):
    template_name = "payment/success.html"


class PaymentFailedView(TemplateView):
    template_name = "payment/failed.html"
