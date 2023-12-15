from django.db import models
from django.contrib.auth.models import AbstractUser
from django.db.models import Sum


class User(AbstractUser):
    first_name = models.CharField(max_length=255, verbose_name='Имя')
    last_name = models.CharField(max_length=255, verbose_name='Фамилия')
    email = models.CharField(max_length=255, unique=True, verbose_name='Электронная почта')
    phone_number = models.CharField(max_length=255, unique=True, verbose_name='Номер телефона')
    username = models.CharField(max_length=255, unique=True, null=True)
    password = models.CharField(max_length=255, null=True, verbose_name='Пароль')

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return str(self.first_name) + " " + str(self.last_name) + " : " + str(self.pk)


class Tag(models.Model):
    title = models.CharField(max_length=255, verbose_name='Название')

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'

    def __str__(self):
        return self.title

class SumOfCredit(models.Model):
    sum = models.FloatField(verbose_name='Сумма')

    class Meta:
        verbose_name = 'Сумма'
        verbose_name_plural = 'Суммы'

    def __str__(self):
        return str(self.sum)


class PeriodOfCredit(models.Model):
    months = models.IntegerField(verbose_name='Количество месяцев')

    class Meta:
        verbose_name = 'Срок кредита'
        verbose_name_plural = 'Сроки кредита'

    def __str__(self):
        return f'{self.months} месяцев'


class Status(models.Model):
    title = models.CharField(max_length=255, verbose_name='Статус')

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'

    def __str__(self):
        return self.title





class Restaurant(models.Model):
    logo = models.ImageField(null=True, verbose_name='Логотип')
    title = models.CharField(max_length=255, verbose_name='Название')
    description = models.TextField(null=True, verbose_name='Описание')
    image = models.ImageField(null=True, verbose_name='Главная фотография')
    tags = models.ManyToManyField(Tag, default=None, verbose_name='Категории', blank=True)
    average = models.CharField(max_length=255, null=True, verbose_name='Средний чек')
    food_type = models.CharField(max_length=255, verbose_name='Тип еды')
    phone_number = models.CharField(max_length=255, verbose_name='Номер телефона')
    menu = models.FileField(null=True, verbose_name='Меню', blank=True)
    sales = models.ImageField(null=True, default=None, verbose_name='Акции')
    prices = models.CharField(null=True, max_length=255, verbose_name='Цены для сертификата')
    slug = models.SlugField(null=True, verbose_name='ссылка')
    location = models.CharField(max_length=255, null=True, verbose_name='Адресс')
    kitchen = models.CharField(max_length=255, null=True, verbose_name='Кухня')
    novy = models.BooleanField(default=False, verbose_name='Скрыть')
    insta = models.CharField(max_length=255, null=True, verbose_name='Instagram')
    whatsapp = models.CharField(max_length=255, null=True, verbose_name='Whatsapp')
    sum_of_credit = models.ManyToManyField(SumOfCredit, default=None, verbose_name='Сумма кредита')

    work_days_1 = models.CharField(max_length=255, null=True, verbose_name='Дни работы 1')
    work_hours_1 = models.CharField(max_length=255, null=True, verbose_name='Часы работы 1')
    work_days_2 = models.CharField(max_length=255, null=True, verbose_name='Дни работы 2')
    work_hours_2 = models.CharField(max_length=255, null=True, verbose_name='Часы работы 2')

    status = models.ForeignKey(Status, on_delete=models.SET_NULL, null=True, blank=True, verbose_name='Статус')

    period_of_credit = models.ManyToManyField(PeriodOfCredit, default=None, verbose_name='Срок кредита')

    restaurant_image = models.ManyToManyField('RestaurantImage', blank=True, default=None, verbose_name='Фотографии')
    class Meta:
        verbose_name = 'Ресторан'
        verbose_name_plural = 'Рестораны'

    def __str__(self):
        return str(self.title)

    def total_order_sum(self):
        total_sum = self.orders.aggregate(total_sum=Sum('sum_of_credit__sum'))['total_sum']
        return total_sum if total_sum is not None else 0


class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    restaurant = models.ForeignKey(Restaurant, on_delete=models.CASCADE, related_name='orders', verbose_name='Ресторан')
    sum_of_credit = models.ForeignKey(SumOfCredit, on_delete=models.CASCADE, verbose_name='Сумма кредита')
    date = models.DateTimeField(auto_now_add=True, verbose_name='Дата')
    period_of_credit = models.ForeignKey(PeriodOfCredit, on_delete=models.CASCADE, verbose_name='Срок кредита')
    status = models.CharField(choices=((1, 'Новые'), (2, 'Активированные'), (3, 'Отказы')), default=1, max_length=255,
                              verbose_name='Статус')

    class Meta:
        verbose_name = 'Заказ'
        verbose_name_plural = 'Заказы'

    def __str__(self):
        return str(self.pk) + ". " + str(self.user) + " : " + str(self.restaurant)


class RestaurantImage(models.Model):
    post = models.ForeignKey(Restaurant, default=None, on_delete=models.CASCADE, null=True, blank=True)
    image = models.ImageField()

    class Meta:
        verbose_name = 'Фотография'
        verbose_name_plural = 'Фотографии'

    def __str__(self):
        return self.post.title
