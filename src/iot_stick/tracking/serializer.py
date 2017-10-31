from rest_framework import serializers
from .models import ModulePostLog, ChannelLog, Module


class ModuleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Module
        fields = ('id', 'module_id')

    def to_representation(self, instance):
        return {
            'module_id': instance.module_id
        }

    def to_internal_value(self, data):
        module_id = data.get('module_id')
        if not module_id:
            raise serializers.ValidationError({
                'module_id': 'This field is required'
            })
        return {
            'module_id': module_id
        }

    def create(self, validated_data):
        module_id = validated_data['module_id']
        return Module.objects.get_or_create(module_id=module_id)


class ChannelLogSerializer(serializers.ModelSerializer):
    datetime = serializers.DateTimeField(input_formats='%Y/%m/%dT%H:%M:%S.%SZ')

    class Meta:
        model = ChannelLog
        fields = ('datetime', 'type', 'value', 'channel')


class ModulePostLogSerializer(serializers.ModelSerializer):

    class Meta:
        model = ModulePostLog
        fields = ('id', 'module', 'type', 'datetime', 'payload')

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

