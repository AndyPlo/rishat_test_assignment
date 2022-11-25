from django.db import models


class Item(models.Model):
    name = models.CharField(
        'Наименование',
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
