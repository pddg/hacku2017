from rest_framework import serializers
from .models import ModulePostLog, ChannelLog, Module, ModuleLocation, Home


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
