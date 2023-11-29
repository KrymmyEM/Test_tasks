from django.db import models

# Create your models here.
#
class Questions(models.Model):
    question = models.TextField(verbose_name="Вопрос")
    answer = models.TextField(null=True, verbose_name="Ответ")
    count = models.IntegerField(verbose_name="Колличество похожих вопросов")

    class Meta:
        db_table='questions'
        verbose_name = 'вопрос'
        verbose_name_plural = 'Вопросы'


class Check_Groups(models.Model):
    groups_id = models.IntegerField(unique=True, verbose_name="ID группы")
    
    class Meta:
        db_table='check_groups'
        verbose_name = 'группу'
        verbose_name_plural = 'Группы телеграмм'


class Check_Channels(models.Model):
    channel_id = models.IntegerField(unique=True, verbose_name="ID канала")
    
    class Meta:
        db_table='check_channels'
        verbose_name = 'канал'
        verbose_name_plural = 'Каналы телеграмм'



class Users(models.Model):
    tg_id = models.IntegerField(unique=True, verbose_name="Индификатор телеграмм")
    admin = models.BooleanField(default=False, verbose_name="Админ пользователь")
    
    class Meta:
        db_table='users'
        verbose_name = 'пользователя'
        verbose_name_plural = 'Пользователи'



class Addresses_Deliver(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    adress = models.TextField()
    
    class Meta:
        db_table='addresses_deliver'
        verbose_name = 'адрес'
        verbose_name_plural = 'Адреса'


class Maillings(models.Model):
    message = models.TextField(null=False, verbose_name="Сообщение")
    photo = models.ImageField(upload_to='maillings_image/', verbose_name="Фотография", null=True)
    get_on_send = models.BooleanField(default=False, verbose_name="Взято в отправку")
    finished = models.BooleanField(default=False, verbose_name="Отправка закончена")
    
    class Meta:
        db_table='maillings'
        verbose_name = 'рассылку'
        verbose_name_plural = 'Рассылки'


