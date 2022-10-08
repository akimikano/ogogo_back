from django.contrib import admin
from apps.hospital.models import *
from apps.users.models import *

admin.site.register(Hospital)
admin.site.register(HospitalUnit)
admin.site.register(WorkerQueue)
admin.site.register(User)
