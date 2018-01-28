from LotAPI.celery import app
from django.core.mail import send_mail
from LotAPI.settings import EMAIL_HOST_USER
from django.utils import timezone
from lotAPP import models


@app.task()
def notify_create_lot(emails, name):
    send_mail('Новые торги',
              'Начались новые торги под названием {0}'.format(name),
              EMAIL_HOST_USER,
              emails,
              )


@app.task()
def notify_new_bet(emails, name, price):
    send_mail('Новая ставка',
              'Новая ставка для {0}, цена составляет {1}'.format(name, price),
              EMAIL_HOST_USER,
              emails,
              )


@app.task()
def notify_close_lot(emails, name, winner):
    send_mail('Аукцион закрылся',
              'Время аукциона "{0}" истекло, победитель {1}'.format(name, winner),
              EMAIL_HOST_USER,
              emails)


@app.task()
def close_lot():
    now = timezone.now()
    open_lots = models.Lot.objects.filter(status=True)
    for lot in open_lots:
        if lot.close_time < now:
            lot.status = False

            try:
                bet_user = lot.bets.get(sum=lot.price).owner
                lot.winner = bet_user
            except models.Bet.DoesNotExist:
                pass
            lot.save()
