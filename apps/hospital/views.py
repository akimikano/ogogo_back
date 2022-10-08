from rest_framework import views, viewsets, mixins
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.decorators import action
from rest_framework.response import Response
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


class WorkerView(viewsets.GenericViewSet):
    serializer_class = WorkerSerializer
    queryset = User.objects.all()

    @action(detail=True, methods=['get'])
    def enter_queue(self, request, pk):
        worker = self.get_object()
        queue, _ = WorkerQueue.objects.get_or_create(worker=worker)
        queue.clients.add(request.user)
        return Response({'success': True})

    @action(detail=True, methods=['get'])
    def quit_queue(self, request):
        worker = self.get_object()
        queue, _ = WorkerQueue.objects.get_or_create(worker=worker)
        queue.clients.remove(request.user)
        return Response({'success': True})


