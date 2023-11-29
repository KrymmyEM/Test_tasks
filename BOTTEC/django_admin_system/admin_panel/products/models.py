from django.db import models
from admin_models.models import Users
# Create your models here.
#

class Categories(models.Model):
    name = models.CharField(max_length=60, verbose_name="Имя категории")
    
    class Meta:
        db_table='categories'
        verbose_name = 'категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.name


class Sub_Categories(models.Model):
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, verbose_name="Номер категории")
    name = models.CharField(max_length=60, verbose_name="Имя подкатегории")
    
    class Meta:
        db_table='sub_categories'
        verbose_name = 'подкатегория'
        verbose_name_plural = 'Подкатегории'

    def __str__(self):
        return self.name


class Items(models.Model):
    sub_category = models.ForeignKey(Sub_Categories, on_delete=models.CASCADE, verbose_name="Номер подкатегории")
    photo = models.ImageField(upload_to="items_images/", verbose_name="Фотография")
    name = models.CharField(max_length=100, verbose_name="Имя товара")
    count = models.IntegerField(verbose_name="Колличество на складе")
    description = models.CharField(max_length=500, verbose_name="Описание")
    price = models.DecimalField(max_digits=8, decimal_places=2, verbose_name="Цена")

    class Meta:
        db_table='items'
        verbose_name = 'товар'
        verbose_name_plural = 'Товары'

    def __str__(self):
        return self.name

class Baskets(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    sell = models.BooleanField(default=False)
    basket_store = models.ManyToManyField(Items, through="Basket_Items")
    
    class Meta:
        db_table='baskets'
        verbose_name = 'корзина'
        verbose_name_plural = 'Корзины'


class Basket_Items(models.Model):
    basket = models.ForeignKey(Baskets, on_delete=models.CASCADE)
    item = models.ForeignKey(Items, on_delete=models.CASCADE)
    count = models.IntegerField(default=1)

    class Meta:
        db_table='basket_items'
        verbose_name = 'элемент корзины'
        verbose_name_plural = 'Элементы корзины'


class Payment_Service(models.Model):
    name = models.CharField(max_length=60)
    
    class Meta:
        db_table='payment_service'
        verbose_name = 'сервис платежа'
        verbose_name_plural = 'Сервисы платежа'

    def __str__(self):
        return self.name

class Payment_Status(models.Model):
    name = models.CharField(max_length=60)
    
    class Meta:
        db_table='payment_status'
        verbose_name = 'статус платежа'
        verbose_name_plural = 'Статусы платежа'

    def __str__(self):
        return self.name


class Oders(models.Model):
    order_id = models.CharField(max_length=55, primary_key=True)
    basket = models.ForeignKey(Baskets, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment_Service, on_delete=models.SET_NULL, null=True)
    payment_status = models.ForeignKey(Payment_Status, on_delete=models.SET_NULL, null=True)
    address_deliver = models.TextField(null=False)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    payment_service_data = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table='orders'
        verbose_name = 'заказ'
        verbose_name_plural = 'Заказы'


