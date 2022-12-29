from django.contrib import admin

# Register your models here.

from .models import Reservation


class ReservationAdmin(admin.ModelAdmin):
    list_display = ['customer_name', 'check_in',
                    'check_out', 'roomNumber', 'roomstatus', ]


admin.site.register(Reservation, ReservationAdmin)
