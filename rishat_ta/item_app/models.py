from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Item(models.Model):
    name = models.CharField(
        'Наименование предмета',
        max_length=200
    )
    description = models.TextField(
        'Описание'
    )
    price = models.DecimalField(
        'Цена',
        max_digits=8,
        decimal_places=2
    )

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'Предмет'
        verbose_name_plural = 'Предметы'


class Tax(models.Model):
    tax_name = models.CharField(
        'Тип налога',
        max_length=50
    )
    tax_amount = models.DecimalField(
        'Налог',
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )
    stripe_tax_rate_id = models.SlugField(
        'Stripe_tax_rate_ID',
        max_length=200,
        unique=True,
        blank=True,
        null=True,
    )

    def __str__(self):
        return f'{self.tax_name}: {self.tax_amount} %'

    class Meta:
        verbose_name = 'Налог'
        verbose_name_plural = 'Налоги'


class Discount(models.Model):
    discount_name = models.CharField(
        'Тип скидки',
        max_length=50
    )
    discount_amount = models.DecimalField(
        'Скидка',
        max_digits=5,
        decimal_places=2,
        validators=[MinValueValidator(0), MaxValueValidator(100)]
    )

    def __str__(self):
        return f'{self.discount_name}: {self.discount_amount} %'

    class Meta:
        verbose_name = 'Скидка'
        verbose_name_plural = 'Скидки'


class Order(models.Model):
    item = models.ManyToManyField(
        Item,
        through='Order_items',
        verbose_name='Наименование предмета'
    )
    discount_amount = models.ForeignKey(
        Discount,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='discounts',
        verbose_name='Скидки'

    )
    tax_amount = models.ForeignKey(
        Tax,
        blank=True,
        null=True,
        on_delete=models.SET_NULL,
        related_name='taxes',
        verbose_name='Налог'
    )

    def __str__(self):
        return f'Заказ №{self.pk}'

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'


class Order_items(models.Model):
    order = models.ForeignKey(
        Order,
        on_delete=models.CASCADE,
        related_name='orders',
        verbose_name='Заказ'
    )
    item = models.ForeignKey(
        Item,
        on_delete=models.CASCADE,
        related_name='items',
        verbose_name='Предметы'
    )
    item_amount = models.IntegerField(
        'Количество предметов'
    )

    def __str__(self):
        return f'{self.order} - {self.item}'

    class Meta:
        verbose_name = 'Предметы в заказе'
        verbose_name_plural = 'Предметы в заказах'
