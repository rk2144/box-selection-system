from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=100)
    length = models.DecimalField(max_digits=8, decimal_places=2)
    width = models.DecimalField(max_digits=8, decimal_places=2)
    height = models.DecimalField(max_digits=8, decimal_places=2)
    weight = models.DecimalField(max_digits=8, decimal_places=3)

    def __str__(self):
        return self.name


class Box(models.Model):
    name = models.CharField(max_length=100)
    inner_length = models.DecimalField(
        max_digits=8, decimal_places=2
    )
    inner_width = models.DecimalField(
        max_digits=8, decimal_places=2
    )
    inner_height = models.DecimalField(
        max_digits=8, decimal_places=2
    )
    max_weight = models.DecimalField(
        max_digits=8, decimal_places=3
    )
    cost = models.DecimalField(
        max_digits=8, decimal_places=2
    )

    def __str__(self):
        return self.name