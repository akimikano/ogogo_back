from rest_framework import views, viewsets, mixins
from django_filters.rest_framework import DjangoFilterBackend

from apps.hospital.serializers import *
from apps.hospital.models import *
from apps.users.models import *


class HospitalView(viewsets.ReadOnlyModelViewSet):
    queryset = Hospital.objects.prefetch_related('hospitalunit_set').all()
    serializer_class = HospitalListSerializer

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return HospitalDetailSerializer
        return HospitalListSerializer


class HospitalUnitView(viewsets.ReadOnlyModelViewSet):
    queryset = HospitalUnit.objects.prefetch_related('workers').all()
    serializer_class = HospitalUnitListSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['hospital']

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return HospitalUnitDetailSerializer
        return HospitalUnitListSerializer


class WorkerQueueView(viewsets.GenericViewSet, mixins.RetrieveModelMixin):
    queryset = User.objects.prefetch_related('hospitalunit_set').all()
    serializer_class = WorkerSerializer



