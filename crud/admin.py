from django.contrib import admin

# Register your models here.
from .models import *

# Register your models here.
admin.site.register(Simulation)
admin.site.register(DashboardMetrics)
admin.site.register(IsSelect)