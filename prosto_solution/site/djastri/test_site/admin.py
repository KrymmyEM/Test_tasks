from django.contrib import admin

from test_site.models import Item, Order, OrderItem, Tax, Discount

admin.site.register(Item)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Tax)
admin.site.register(Discount)

# Register your models here.
