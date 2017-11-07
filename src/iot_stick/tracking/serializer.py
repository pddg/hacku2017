from rest_framework import serializers
from django.contrib.gis.geos import Point
from django.contrib.gis.db.models.functions import Distance
from .models import ModulePostLog, ChannelLog, Module, ModuleLocation, Home, StateChoices


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ('pk', 'module_id')


class ChannelLogSerializer(serializers.ModelSerializer):
    datetime = serializers.DateTimeField(input_formats='%Y/%m/%dT%H:%M:%S.%fZ')

    class Meta:
        model = ChannelLog
        fields = ('datetime', 'type', 'value', 'channel')


class ModulePostLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = ModulePostLog
        fields = ('module', 'type', 'datetime', 'payload')

    def to_representation(self, instance):
        return {
            'module': instance.module.module_id,
            'type': instance.type,
            'datetime': instance.datetime,
            'payload': {
                'channels': [ChannelLogSerializer(ch).data for ch in instance.payload.all()]
            }
        }

    def to_internal_value(self, data):
        key_array = ['module', 'type', 'datetime', 'payload']
        results = {}
        for key in key_array:
            if key != 'payload':
                val = data.get(key)
            else:
                val = data.get(key)['channels']
            if not val:
                raise serializers.ValidationError({
                    key: 'This field is required'
                })
            results[key] = val
        return results

    def create(self, validated_data):
        module_id = validated_data.pop('module')
        module_, _ = Module.objects.get_or_create(module_id=module_id)
        payload = validated_data.pop('payload')
        log = ModulePostLog.objects.create(module=module_, **validated_data)
        for channel in payload:
            ChannelLog.objects.create(module_log=log, **channel)
        channels = log.payload.order_by("channel").all()
        # 変な値が紛れ込まないようチェック
        # channel数が3以外の時は値が余計 or 足りない
        if channels.count() != 3:
            return log
        # 値の型チェック
        if channels[1].type != "f" or channels[0].type != "f" or channels[2].type != "I":
            return log
        # 緯度経度の範囲に収まっているか
        if 90 < channels[0].value or channels[0].value < -90 or -180 > channels[1].value or channels[1].value > 180:
            return log
        # 杖の倒れた判定は0か1のみ
        if channels[2].value > 1 or channels[2].value < 0:
            return log
        # 現在の最新のlocationを取得
        previous_location = ModuleLocation.objects.filter(module=module_).order_by('-created_on').first()
        # 新しいlocationを作成
        current_location = ModuleLocation.objects.create(
            created_on=log.datetime,
            is_knocked_down=int(channels[2].value),
            geom=Point(channels[1].value, channels[0].value, srid=4326),
            module=module_
        )
        current_location.save()
        # 無ければ即リターン
        if previous_location is None:
            return log
        previous_state = previous_location.state
        # 各homeからの距離を取得
        i = 0
        determined = list()
        for home in Home.objects.filter(module=module_).annotate(distance=Distance('geom', current_location.geom)):
            # 設定された半径内にいるかどうかの判定
            distance_meter = home.distance.km * 1000
            is_not_within = distance_meter > home.radius
            determined.append({
                'is_not_within': is_not_within,
                'diff': distance_meter - home.radius,
                'home': home.name,
                'radius': home.radius
            })
            if is_not_within:
                i += 1
        # homeが登録されていないとき
        if len(determined) == 0:
            return log
        # (homeの中心からの距離) - (設定した半径)の昇順に並べる
        determined = sorted(determined, key=lambda x: x['diff'])
        # 1つでも範囲内に入っていればリターン
        if len(determined) != i:
            if previous_state == StateChoices.OUT.value:
                from .tasks import send_outgoing_webhook
                send_outgoing_webhook.delay(
                    module_id,
                    current_location.state,
                    determined[0]['home'],
                    determined[0]['radius'],
                    False
                )
            return log
        # 全てのHomeについて設定の範囲外にいる場合
        current_location.state = StateChoices.OUT.value
        current_location.save()
        if previous_state == StateChoices.IN.value:
            from .tasks import send_outgoing_webhook
            send_outgoing_webhook.delay(
                module_id,
                current_location.state,
                determined[0]['home'],
                determined[0]['radius'],
                True
            )
        return log


class ModuleLocationSerializer(serializers.ModelSerializer):
    module = serializers.SerializerMethodField('get_module_id')
    created_on = serializers.DateTimeField(input_formats='%Y/%m/%dT%H:%M:%S.%fZ', default_timezone='Asia/Tokyo')

    class Meta:
        model = ModuleLocation
        fields = ('geom', 'created_on', 'module')

    def get_module_id(self, obj):
        return obj.module.module_id


class HomeSerializer(serializers.ModelSerializer):
    module = serializers.SerializerMethodField('get_module_id')

    class Meta:
        model = Home
        fields = ('module', 'geom', 'name', 'radius')

    def get_module_id(self, obj):
        return obj.module.module_id
