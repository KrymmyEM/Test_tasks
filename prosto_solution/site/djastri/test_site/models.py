import uuid

from django.conf import settings
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser
import stripe
# Create your models here.

#TODO: ADD All verbonse_name on russian language in editable fields

#user model use abstract user
class User(AbstractUser):
    pass


class Item(models.Model):
    name = models.CharField(max_length=500, null=False, verbose_name='Наименование')
    description = models.TextField(null=True, verbose_name='Описание')
    price = models.IntegerField(null=False, validators=[
        MinValueValidator(0)
    ], verbose_name='Цена')
    stripe_product_id = models.CharField(max_length=500, null=True, editable=False)
    stripe_price_id = models.CharField(max_length=500, null=True, editable=False)

    def __str__(self):
        return str(self.pk) + "|" + str(self.name)

    def save(self,*args, **kwargs):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        #create stripe product
        stripe_product = stripe.Product.create(name=self.name)
        self.stripe_product_id = stripe_product['id']

        #create stripe price
        stripe_price = stripe.Price.create(
            product=stripe_product['id'],
            unit_amount=self.price,
            currency='rub',
        )
        self.stripe_price_id = stripe_price['id']
        super(Item, self).save(*args, **kwargs)


# discount model, name, percent_off, stripe_coupone_id
class Discount(models.Model):
    name = models.CharField(max_length=500, null=False, verbose_name='Наименование')
    percent_off = models.IntegerField(null=False, validators=[
        MaxValueValidator(100),
        MinValueValidator(0)
    ], verbose_name='Процент скидки')
    stripe_coupon_id = models.CharField(max_length=500, null=True, editable=False)

    def __str__(self):
        return str(self.pk) + "|" + str(self.name)

    def save(self,*args, **kwargs):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        #create stripe coupon
        stripe_coupon = stripe.Coupon.create(
            percent_off=self.percent_off,
            duration='forever',
            name=self.name,
            currency='rub',
        )
        self.stripe_coupon_id = stripe_coupon['id']
        super(Discount, self).save(*args, **kwargs)


# tax model, display_name, percentage (0..100), description (null True), stripe_tax_rate_id
class Tax(models.Model):
    display_name = models.CharField(max_length=500, null=False, verbose_name='Отображаемое имя')
    percentage = models.IntegerField(null=False, validators=[
        MaxValueValidator(100),
        MinValueValidator(0)
    ], verbose_name='Процент')
    description = models.TextField(null=True, verbose_name='Описание')
    stripe_tax_rate_id = models.CharField(max_length=500, null=True, editable=False)

    def __str__(self):
        return str(self.pk) + "|" + str(self.display_name)

    def save(self,*args, **kwargs):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        #create stripe tax rate
        stripe_tax_rate = stripe.TaxRate.create(
            display_name=self.display_name,
            description=self.description,
            percentage=self.percentage,
            currency='rub',
        )
        self.stripe_tax_rate_id = stripe_tax_rate['id']
        super(Tax, self).save(*args, **kwargs)


# order model, uuid, discounts, tax, in_work, stripe_checkout_session_id, stripe_payment_intent_id
class Order(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    discounts = models.ForeignKey(Discount, on_delete=models.SET_NULL, null=True, verbose_name='Скидка')
    tax = models.ForeignKey(Tax, on_delete=models.SET_NULL, null=True, verbose_name='Налог')
    in_work = models.BooleanField(null=False, default=False, verbose_name='В работе')
    stripe_checkout_session_id = models.CharField(max_length=500, null=True, unique=True, editable=False)
    stripe_payment_intent_id = models.CharField(max_length=500, null=True, unique=True, editable=False)
    orderitem_set = models.ManyToManyField(Item, through='OrderItem', related_name='order_items')

    def __str__(self):
        return str(self.pk) + "|" + str(self.user) 

    def save(self,*args, **kwargs):
        super(Order, self).save(*args, **kwargs)


# order_item model, order, item, quantity
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, verbose_name='Заказ', related_name='orders')
    item = models.ForeignKey(Item, on_delete=models.CASCADE, verbose_name='Предмет', related_name='items')
    quantity = models.IntegerField(validators=[
        MinValueValidator(1)
    ], default=1, verbose_name='Количество')

    def __str__(self):
        return str(self.id)

    def save(self,*args, **kwargs):
        super(OrderItem, self).save(*args, **kwargs)