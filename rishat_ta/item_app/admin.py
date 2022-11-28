from django.contrib import admin

from .models import Discount, Item, Order, Order_items, Tax


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'description', 'price')
    list_editable = ('price', )


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('pk', 'discount_name', 'discount_amount')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('pk', 'discount_amount', 'tax_amount')


@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = ('pk', 'tax_name', 'tax_amount', 'stripe_tax_rate_id')


@admin.register(Order_items)
class OrderItemsAdmin(admin.ModelAdmin):
    list_display = ('order', 'item', 'item_amount')
    list_editable = ('item_amount', )
