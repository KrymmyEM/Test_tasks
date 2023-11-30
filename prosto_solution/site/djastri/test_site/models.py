import uuids

from django.conf import settings
from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser
import stripe
# Create your models here.

#user model use abstract user
class User(AbstractUser):
    pass


class Item(models.Model):
    name = models.CharField(max_length=500, null=False)
    description = models.TextField(null=True)
    price = models.IntegerField(null=False, validators=[
        MinValueValidator(0)
    ])
    stripe_product_id = models.CharField(max_length=500, null=True)
    stripe_price_id = models.CharField(max_length=500, null=True)

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
            currency='usd',
        )
        self.stripe_price_id = stripe_price['id']
        super(Item, self).save(*args, **kwargs)


# discount model, name, percent_off, stripe_coupone_id
class Discount(models.Model):
    name = models.CharField(max_length=500, null=False)
    percent_off = models.IntegerField(null=False, validators=[
        MaxValueValidator(100),
        MinValueValidator(0)
    ])
    stripe_coupon_id = models.CharField(max_length=500, null=True)

    def __str__(self):
        return str(self.pk) + "|" + str(self.name)

    def save(self,*args, **kwargs):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        #create stripe coupon
        stripe_coupon = stripe.Coupon.create(
            percent_off=self.percent_off,
            duration='once',
        )
        self.stripe_coupon_id = stripe_coupon['id']
        super(Discount, self).save(*args, **kwargs)


# tax model, display_name, percentage (0..100), description (null True), stripe_tax_rate_id
class Tax(models.Model):
    display_name = models.CharField(max_length=500, null=False)
    percentage = models.IntegerField(null=False, validators=[
        MaxValueValidator(100),
        MinValueValidator(0)
    ])
    description = models.TextField(null=True)
    stripe_tax_rate_id = models.CharField(max_length=500, null=True)

    def __str__(self):
        return str(self.pk) + "|" + str(self.display_name)

    def save(self,*args, **kwargs):
        stripe.api_key = settings.STRIPE_SECRET_KEY
        #create stripe tax rate
        stripe_tax_rate = stripe.TaxRate.create(
            display_name=self.display_name,
            description=self.description,
            percentage=self.percentage,
        )
        self.stripe_tax_rate_id = stripe_tax_rate['id']
        super(Tax, self).save(*args, **kwargs)


# order model, uuid, discounts, tax, sell, stripe_checkout_session_id, stripe_payment_intent_id
class Order(models.Model):
    uuid = models.UUIDField(unique=True, default=uuid.uuid4, editable=False, primary_key=True)
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    discounts = models.ForeignKey(Discount, on_delete=models.SET_NULL, null=True)
    tax = models.ForeignKey(Tax, on_delete=models.SET_NULL, null=True)
    to_action = models.BooleanField(null=False, default=False)
    stripe_checkout_session_id = models.CharField(max_length=500, null=True, unique=True)
    stripe_payment_intent_id = models.CharField(max_length=500, null=True, unique=True)
    orderitem_set = models.ManyToManyField(Item, through='OrderItem')

    def __str__(self):
        return str(self.pk) + "|" + str(self.user) 

    def save(self,*args, **kwargs):
        super(Order, self).save(*args, **kwargs)


# order_item model, order, item, quantity
class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.CASCADE)
    quantity = models.IntegerField(validators=[
        MinValueValidator(1)
    ], default=1)

    def __str__(self):
        return str(self.id)

    def save(self,*args, **kwargs):
        super(OrderItem, self).save(*args, **kwargs)