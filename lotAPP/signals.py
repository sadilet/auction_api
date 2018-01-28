from django.dispatch import receiver
from lotAPP.models import Lot, User
from django.db.models.signals import post_save
from rest_framework.authtoken.models import Token
from django.conf import settings
from lotAPP.tasks import *


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)


@receiver(post_save, sender=Lot)
def mail_send_newLot(instance, created=False, **kwargs):
    if created:
        lot_name = instance.name
        emails = User.objects.all().exclude(pk=instance.author.pk).values_list('email', flat=True)
        notify_create_lot.delay(list(emails), lot_name)

    if instance.status == True:
        lot_name = instance.name
        lot_price = instance.price
        emails = set(User.objects.filter(bet__lot=instance.id).values_list('email', flat=True))
        notify_new_bet.delay(list(emails), lot_name, lot_price)

    if instance.status == False:
        emails = set(User.objects.filter(bet__lot=instance.id).values_list('email', flat=True))
        notify_close_lot.delay(list(emails), instance.name, instance.winner.username)
