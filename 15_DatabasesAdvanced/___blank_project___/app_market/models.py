from decimal import Decimal

from django.contrib.auth.models import User
from django.db import models


class Shop(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    
    def __str__(self):
        return f'[{self.id}] {self.title}'
    
    class Meta:
        verbose_name = 'магазин'
        verbose_name_plural = 'магазины'
        ordering = ['title']
        db_table = 'shops'


class Good(models.Model):
    title = models.CharField(
        max_length=200,
        verbose_name='Название'
    )
    description = models.CharField(
        max_length=500,
        verbose_name='Описание'
    )
    shop = models.ForeignKey(
        Shop,
        related_name='shop_good',
        verbose_name='Магазин',
        on_delete=models.CASCADE
    )
    price = models.FloatField(
        verbose_name='Цена',
        default=0
    )
    face_image = models.ImageField(
        upload_to='images/goods/',
        null=True,
        blank=True
    )
    remains = models.IntegerField(
        verbose_name='Остаток',
        default=0
    )
    
    # def get_image_from_url(self, url, new_name):
    #     img_tmp = NamedTemporaryFile(delete=True)
    #     with urlopen(url) as uo:
    #         assert uo.status == 200
    #         img_tmp.write(uo.read())
    #         img_tmp.flush()
    #     img = File(img_tmp)
    #     self.face_image.save(new_name, img)
    
    def __str__(self):
        return f'[{self.id}] {self.title} ({self.price})'
    
    class Meta:
        verbose_name = 'товар'
        verbose_name_plural = 'товары'
        ordering = ['title']
        db_table = 'goods'


class GoodImages(models.Model):
    good = models.ForeignKey(
        Good,
        verbose_name='Товар',
        related_name='image_good_images',
        on_delete=models.CASCADE
    )
    image = models.ImageField(
        upload_to='images/goods/',
        null=True,
        blank=True
    )
    
    # def get_image_from_url(self, url, new_name):
    #     img_tmp = NamedTemporaryFile(delete=True)
    #     with urlopen(url) as uo:
    #         assert uo.status == 200
    #         img_tmp.write(uo.read())
    #         img_tmp.flush()
    #     img = File(img_tmp)
    #     self.image.save(new_name, img)
    
    def __str__(self):
        return f'[{self.id}] {self.good}, {self.image}'
    
    class Meta:
        verbose_name = 'изображение'
        verbose_name_plural = 'изображения'
        ordering = ['id']
        db_table = 'good_images'


class Order(models.Model):
    user = models.ForeignKey(
        User,
        related_name='user_order',
        on_delete=models.CASCADE,
        verbose_name='Пользователь'
    )
    create_at = models.DateTimeField(
        auto_now_add=True,
        verbose_name='Дата формирования заказа'
    )
    paid_at = models.DateTimeField(
        auto_now_add=False,
        blank=True,
        null=True,
        verbose_name='Дата оплаты заказ'
    )
    
    def __str__(self):
        paid = ''
        if self.paid_at is not None:
            paid = f' > {self.paid_at.strftime("%d.%m.%Y %H:%M:%S")}'
        return f'[{self.id}] {self.user.username}, {self.create_at.strftime("%d.%m.%Y %H:%M:%S")}{paid}'
    
    def total_paid(self):
        return sum(
            Decimal(item['price']) * Decimal(item['amount']) for item in self.order_item.values()
        )
    
    class Meta:
        verbose_name = 'наряд-заказ'
        verbose_name_plural = 'наряд-заказы'
        ordering = ['create_at']
        db_table = 'orders'


class OrderItem(models.Model):
    order = models.ForeignKey(
        Order,
        related_name='order_item',
        on_delete=models.CASCADE,
        verbose_name='Заказ'
    )
    good = models.ForeignKey(
        Good,
        related_name='good_order_item',
        on_delete=models.CASCADE,
        verbose_name='Товар'
    )
    price = models.FloatField(
        verbose_name='Цена на момент заказа',
        default=0
    )
    amount = models.FloatField(
        verbose_name='Количество',
        default=1
    )
    
    def get_total_price(self):
        return self.price * self.amount
    
    def __str__(self):
        return f'[{self.id}] {self.order.id}, {self.good.title} - {self.price}'
    
    class Meta:
        verbose_name = 'товар в заказе'
        verbose_name_plural = 'товары заказа'
        ordering = ['id']
        db_table = 'order_items'
