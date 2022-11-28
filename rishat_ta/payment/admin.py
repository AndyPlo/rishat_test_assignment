from django.contrib import admin
from .models import Item, Discount, Order, Tax, Item_order


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
    list_display = ('pk', 'name', 'description', 'price')


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = ('pk', 'discount_amount')


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('pk', 'discount_amount', 'tax_amount')


@admin.register(Tax)
class TaxAdmin(admin.ModelAdmin):
    list_display = ('pk', 'tax_name', 'tax_amount')


@admin.register(Item_order)
class ItemOrderAdmin(admin.ModelAdmin):
    list_display = ('order', 'item', 'item_amount')
    list_editable = ('item',)
