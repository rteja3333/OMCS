from django.contrib import admin
from .models import hospital,doctor,patient,appointments,bookedappointments,pending_doctors,Admin
admin.site.register(hospital)
admin.site.register(doctor)
admin.site.register(patient)
admin.site.register(appointments)
admin.site.register(bookedappointments)

admin.site.register(pending_doctors)
admin.site.register(Admin)

# Register your models here.
