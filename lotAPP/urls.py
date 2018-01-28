from django.conf.urls import url
from .views import \
    (CreateUser,
     LotListCreate,
     OneInfoLot,
     BetOnLot,
     MyBets,
     )

urlpatterns = [
    url(r'^bets/$', MyBets.as_view(), name='MyBets'),
    url(r'^lots/(?P<pk>\d+)/bets', BetOnLot.as_view(), name='betOnLot'),
    url(r'^lots/(?P<pk>\d+)/$', OneInfoLot.as_view(), name='info-lot'),
    url(r'^lots/$', LotListCreate.as_view(), name='all lots'),
    url(r'^register/$', CreateUser.as_view(), name='register'),
]
