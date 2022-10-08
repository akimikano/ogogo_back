from rest_framework import serializers
from apps.hospital.models import *
from apps.users.serializers import UserBasicSerializer
from apps.users.models import *


class HospitalUnitListSerializer(serializers.ModelSerializer):
    class Meta:
        model = HospitalUnit
        fields = (
            'id', 'name', 'hospital'
        )


class HospitalUnitDetailSerializer(serializers.ModelSerializer):
    workers = UserBasicSerializer(many=True)

    class Meta:
        model = HospitalUnit
        fields = (
            'id', 'name', 'hospital', 'workers'
        )


class HospitalListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Hospital
        fields = (
            'id', 'name', 'address'
        )


class HospitalDetailSerializer(serializers.ModelSerializer):
    units = HospitalUnitListSerializer(source='hospitalunit_set', many=True)

    class Meta:
        model = Hospital
        fields = (
            'id', 'name', 'address', 'units'
        )


class WorkerSerializer(serializers.ModelSerializer):
    units = serializers.SerializerMethodField()

    class Meta:
        model = User
        fields = (
            'id', 'username', 'first_name', 'last_name', 'units'
        )

    def get_units(self, obj):
        units = obj.hospitalunit_set.all()
        serializer = HospitalUnitListSerializer(units, many=True, context=self.context)
        return serializer.data


class WorkerQueueSerializer(serializers.ModelSerializer):
    clients = UserBasicSerializer(many=True)

    class Meta:
        model = WorkerQueue
        fields = (
            'id', 'clients'
        )

