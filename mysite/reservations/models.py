from django.db import models
from django.conf import settings
from rooms.models import Room
from django.urls import reverse
from django.utils import timezone
from django.core.exceptions import ValidationError
from datetime import datetime, date, timedelta
import math
from django.contrib.postgres.fields import DateRangeField
from django.utils import timezone

# Create your models here.


class Reservation(models.Model):
    # is_cleaned = False

    discount_types = (
        (None, 'No Discount'),
        ('10', '10%'),
        ('20', '20%'),
        ('30', '30%'),
        ('Oth', 'Other'),
    )

    room_stat_types = (
        ('reserve', 'reserve'),
        ('checkin', 'checkin'),
        ('checkout', 'checkout'),
    )

    roomstatus = models.CharField(
        max_length=20, choices=room_stat_types, null=True, blank=True, default='reserve')
    discount = models.CharField(
        max_length=20, choices=discount_types, null=True, blank=True, default='Oth')
    room_price = models.IntegerField(null=True, blank=True)
    check_in = models.DateTimeField(
        blank=True, null=True)
    # check_in_in = models.DateTimeField(blank=True, null=True)
    check_out = models.DateTimeField(
        blank=True, null=True)
    book_date = models.DateTimeField(default=timezone.now)
    customer_name = models.CharField(max_length=225)
    customer_address = models.CharField(max_length=225)
    customer_number = models.IntegerField(null=True)
    no_of_days = models.IntegerField(null=True, blank=True)
    checking_in_now = models.BooleanField(default=False)
    total_cost = models.IntegerField()
    extra_field = models.IntegerField(null=True, blank=True, default=None)

    roomNumber = models.ForeignKey(
        Room, related_name="guest_reserve", on_delete=models.CASCADE)  # reservations
    # payment = models.ForeignKey(
    #     Room, related_name="guest_pay", on_delete=models.CASCADE)

    pay_types = (
        ('P', 'Paying'),
        ('PD', 'Paying Debtor'),
        ('NP', 'Non Paying'),
    )

    mode_pay_types = (
        ('C', 'Cash'),
        ('P', 'POS'),
        ('TF', 'Transfer'),
    )
    payment_type = models.CharField(
        max_length=20, choices=pay_types, default="NP")
    paid_date = models.DateTimeField(blank=True, null=True, default=None)
    payment_mode = models.CharField(
        max_length=20, choices=mode_pay_types, null=True, blank=True)

    credit_balance = models.IntegerField(default=0)

    # debt_paid_types = (
    #     ('Y', 'Yes'),
    #     ('N', 'No'),
    # )
    # debt_paid = models.CharField(
    #     max_length=20, choices=pay_types, default=None)

    # def guest_paid(self):
    #     # or create a button.Once clicked,pay_type becomes P and paid date is updated.
    #     if self.pay_types == "P":
    #         self.paid_date = datetime.now()

    def __str__(self):
        return self.customer_name

    # def clean(self):
    #     self.is_cleaned = True
    #     bookingList = Reservation.objects.filter(roomNumber=self.roomNumber)
    #     for booking in bookingList:
    #         if booking.check_in >= self.check_out or booking.check_out <= self.check_in:
    #             pass
    #         else:
    #             raise ValidationError("Change Date")

    #     if self.check_out < self.check_in:
    #         raise ValidationError("Check out can't be less than Check In")
    #     super(Reservation, self).clean()
    def checkin(self):
        self.check_in = timezone.now()
        self.roomstatus = 'checkin'
        # print(math.ceil(int((
        #     self.check_out - self.check_in).total_seconds())/60/60/24))

        self.save()

    def checkout(self):
        self.check_out = timezone.now()
        self.roomstatus = 'checkout'
        self.save()
    # checking radion button when form is being filled

    def check_in_now(self):
        if self.checking_in_now == True:
            self.roomstatus = 'checkin'
        self.save()

    def paid_date_update(self):
        if self.payment_type == 'P':
            self.paid_date == datetime.now()
        # self.save()

    def value(self):
        if self.discount == '10':
            price = self.roomNumber.roomtype.price
            x = (price - (price*0.1))
            return x
        if self.discount == '20':
            price = self.roomNumber.roomtype.price
            x = (price - (price*0.2))
            return x
        if self.discount == '30':
            price = self.roomNumber.roomtype.price
            x = (price - (price*0.3))
            return x
        if self.discount == None:
            x = self.roomNumber.roomtype.price
            return x
        # self.save()

    def no_of_days_booked(self):
        #     self.no_of_days = (self.check_out - self.check_in).days
        test_value = (self.check_out - self.check_in).total_seconds()/60/60/24
        math.modf(test_value)
        if (math.modf(test_value)[0] > 0 and math.modf(test_value)[0] < 1):
            return math.modf(test_value)[1] + 1

        else:
            return math.modf(test_value)[1]

    # def cdt_balance(self):
    #     if self.no_of_days == 1 and (self.book_date == self.check_in):
    #         credit_total = 0
    #         return credit_total
    #     if self.no_of_days > 1 and (self.book_date == self.check_in):
    #         credit_total = self.total_cost - self.room_price
    #         return credit_total
    #     if self.book_date < self.check_in and self.payment_type == "P":
    #         credit_total = self.total_cost
    #         return credit_total

    def save(self, *args, **kwargs):
        # print(datetime.now().date())
        # print(timezone.now().date())
        # self.check_in_now()
        if self.roomstatus == 'checkin' and datetime.now.date() < self.check_out:
            self.credit_balance = self.credit_balance - self.room_price

        if self.id:
            print('updating')
        else:
            print('creating')
        self.no_of_days = self.no_of_days_booked()
        self.room_price = self.value()
        self.total_cost = self.no_of_days * self.room_price
        self.credit_balance = self.total_cost
        self.paid_date_update()
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('reservations:all')


# class Payment(models.Model):

#     pay_types = (
#         ('P', 'Paying'),
#         ('PD', 'Paying Debtor'),
#         ('NP', 'Non Paying'),
#     )

#     mode_pay_types = (
#         ('C', 'Cash'),
#         ('P', 'POS'),
#         ('TF', 'Transfer'),
#     )

#     paid_date = models.DateTimeField(blank=True, null=True)
#     payment_mode = models.CharField(
#         max_length=20, choices=mode_pay_types, null=True, blank=True)
#     payment_type = models.CharField(
#         max_length=20, choices=pay_types, default="NP")
#     credit_balance = models.IntegerField()

#     def guest_paid(self):
#         # or create a button.Once clicked,pay_type becomes P and paid date is updated.
#         if self.pay_types == "P":
#             self.paid_date = datetime.now()

#     def save(self, *args, **kwargs):
#         self.credit_balance = self.total_cost


#         super().save(*args, **kwargs)
