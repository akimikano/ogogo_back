from rest_framework.routers import DefaultRouter
from . import views

hospital_router = DefaultRouter()
hospital_router.register(r'hospitals', views.HospitalView)
hospital_router.register(r'hospital_units', views.HospitalUnitView)
