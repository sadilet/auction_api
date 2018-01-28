from rest_framework import serializers
from django.contrib.auth.models import User
from lotAPP.models import Lot, Bet
from django.utils import timezone
from rest_framework.serializers import ValidationError


class UserSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, allow_blank=False, style={'input_type': 'password'})
    email = serializers.EmailField(allow_blank=False)

    class Meta:
        model = User
        fields = ('username', 'password', 'email')


class LotSerializer(serializers.ModelSerializer):
    author = serializers.SlugRelatedField(read_only=True, slug_field='username')
    status = serializers.BooleanField(read_only=True)

    def validate_close_time(self, value):
        now = timezone.now()
        print(now)
        if value <= now:
            raise ValidationError('Время закрытия')
        return value

    class Meta:
        model = Lot
        fields = ('author', 'id', 'name', 'price', 'price_step', 'text', 'status', 'close_time')


class BetSerializer(serializers.ModelSerializer):
    lot = serializers.SlugRelatedField(read_only=True, slug_field='name')
    owner = serializers.ReadOnlyField(source='owner.username')

    def validate(self, data):
        lot = Lot.objects.get(id=self.context['pk'])
        if not lot.status:
            raise ValidationError('Аукцион закрыт')
        bet_user = self.context['request'].user
        if bet_user == lot.author:
            raise ValidationError('Вы не можете сделать ставку, так как являетесь создателем аукциона')
        sum_bet = data['sum']
        if sum_bet <= lot.price:
            raise ValidationError('Сумма ставки меньше существующей цены')
        if (sum_bet - lot.price) % lot.price_step != 0:
            raise ValidationError('Сумма ставки не соответсвует параметрам ставки')
        return data

    class Meta:
        model = Bet
        fields = ('lot', 'owner', 'sum',)


class LotAndBetSerializer(serializers.ModelSerializer):
    bets = BetSerializer(many=True, read_only=True)
    author = serializers.SlugRelatedField(read_only=True, slug_field='username')

    class Meta:
        model = Lot
        fields = ('id', 'name', 'author', 'price', 'price_step', 'text', 'status', 'bets',)
