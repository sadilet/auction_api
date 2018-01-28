from rest_framework import status
from rest_framework.response import Response
from .serializers import UserSerializer, LotSerializer, BetSerializer, LotAndBetSerializer
from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveAPIView, ListCreateAPIView
from rest_framework.permissions import AllowAny
from .models import Lot, Bet
from django.contrib.auth.hashers import make_password


class CreateUser(CreateAPIView):
    permission_classes = (AllowAny,)
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        password = make_password(self.request.data['password'])
        return serializer.save(password=password)


class LotListCreate(ListCreateAPIView):
    serializer_class = LotSerializer
    queryset = Lot.objects.all()
    filter_fields = ('status',)

    def perform_create(self, serializer):
        return serializer.save(author=self.request.user)


class OneInfoLot(RetrieveAPIView):
    queryset = Lot.objects.all()
    serializer_class = LotAndBetSerializer


class BetOnLot(ListCreateAPIView):
    serializer_class = BetSerializer

    def get_queryset(self):
        return Bet.objects.filter(lot=self.kwargs.get('pk'))

    def post(self, request, *args, **kwargs):
        serializer = BetSerializer(data=request.data, context={"pk": kwargs.get('pk'), "request": self.request})
        if serializer.is_valid():
            serializer.save(owner=self.request.user, lot=Lot.objects.get(pk=self.kwargs['pk']))
            return Response(data=serializer.data, status=status.HTTP_201_CREATED)

        serializer.is_valid(raise_exception=True)


class MyBets(ListAPIView):
    serializer_class = BetSerializer

    def get_queryset(self):
        return Bet.objects.filter(owner=self.request.user)
