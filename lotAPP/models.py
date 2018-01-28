from django.db import models, transaction
from django.contrib.auth.models import User

CHOICES = ((True, 'Активный'), (False, 'Завершенный'))


class Lot(models.Model):
    class Meta:
        verbose_name = 'Лот'
        verbose_name_plural = 'Лоты'

    author = models.ForeignKey(User, verbose_name='Создатель', related_name='author')
    name = models.CharField(max_length=50, verbose_name='Название лота', blank=False)
    price = models.BigIntegerField(verbose_name='Цена', blank=False)
    price_step = models.IntegerField(verbose_name='Шаг цены', blank=False)
    text = models.TextField(verbose_name='Описание лота', max_length=200, blank=False)
    status = models.BooleanField(choices=CHOICES, default=True, verbose_name='Статус')
    close_time = models.DateTimeField(verbose_name="Дата закрытия", blank=False, auto_now_add=True)
    winner = models.ForeignKey(User, verbose_name='Победитель', related_name='winner', null=True, blank=True)

    def __str__(self):
        return "%s" % self.name


class Bet(models.Model):
    class Meta:
        verbose_name = 'Ставка'
        verbose_name_plural = 'Ставки'

    owner = models.ForeignKey(User, verbose_name='Автор ставки')
    lot = models.ForeignKey(Lot, verbose_name='Выберите лот для ставки', related_name='bets')
    sum = models.IntegerField(verbose_name='Сумма ставки', blank=False)

    def __str__(self):
        return "%s" % self.owner

    @transaction.atomic
    def save(self, *args, **kwargs):
        self.lot.price = self.sum
        self.lot.save()
        super(Bet, self).save(*args, **kwargs)

