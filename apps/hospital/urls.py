from rest_framework.routers import DefaultRouter
from . import views

hospital_router = DefaultRouter()
hospital_router.register(r'hospitals', views.HospitalView)
hospital_router.register(r'hospital_units', views.HospitalUnitView)
hospital_router.register(r'workers', views.WorkerView)
hospital_router.register(r'clients', views.ClientView)
