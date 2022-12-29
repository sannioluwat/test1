from django import forms
from . import models
from reservations.models import Reservation
from datetime import datetime, date, timedelta
from django.core.exceptions import ValidationError
from django.utils import timezone


class ReservationForm(forms.ModelForm):

    class Meta:
        model = models.Reservation
        fields = 'discount', 'extra_field', 'check_in', 'check_out', 'customer_name', 'customer_address', 'customer_number', 'checking_in_now', 'roomNumber', 'payment_type', 'payment_mode'

        exclude = {'roomstatus',
                   'no_of_days', 'room_price', 'book_date', 'total_cost', 'credit_balance', 'paid_date'}

        widgets = {
            'check_in': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'check_out': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),

        }

    def clean(self):
        print(self.instance.id)
        data = self.cleaned_data
        discount = data['discount']
        # if discount == 'Oth':
        #     self.exclude('extra_link')
        check_in = data['check_in']
        check_out = data['check_out']
        roomNumber = data['roomNumber']
        customer_name = data['customer_name']
        payment_type = data['payment_type']
        payment_mode = data['payment_mode']
        if (payment_type == 'PD' and payment_mode is not None) or (payment_type == 'NP' and payment_mode is not None):
            raise forms.ValidationError(
                "A non-paying or paying debtor can't select mode of payment")

        # print(datetime.today().timestamp())
        # if check_in.timestamp() < datetime.today().timestamp():
        "A non-paying or paying debtor can't select mode of payment"

        if check_in.date() < timezone.now().date():

            raise forms.ValidationError("check-in date can't be before today")

        if self.instance.id:

            bookingList = Reservation.objects.filter(
                roomNumber=roomNumber).exclude(id=self.instance.id)
            for booking in bookingList:
                if booking.check_in >= check_out or booking.check_out <= check_in:
                    pass
                else:
                    raise ValidationError("Change Date")
            if check_out < check_in:
                raise forms.ValidationError(
                    "End date should be greater than start date.")
            return data
        else:

            bookingList = Reservation.objects.filter(
                roomNumber=roomNumber)
            for booking in bookingList:
                if booking.check_in >= check_out or booking.check_out <= check_in:
                    pass
                else:
                    raise ValidationError("Change Date")
            if check_out < check_in:
                raise forms.ValidationError(
                    "End date should be greater than start date.")
            return data

    def __init__(self, *args, **kwargs):
        # discount = kwargs.pop('discount')
        enable_my_bool = kwargs.pop('discount', True)

        super().__init__(*args, **kwargs)
        # if self.fields['discount'] == (None or '10' or '20' or '30'):
        # del self.fields['extra_field']
        # self.fields.pop('extra_field')
        # print('yes')
        if not enable_my_bool:
            self.fields.pop('extra_field')
# class PaymentForm(forms.ModelForm):
#     class Meta:
#         model = models.Payment
#         fields = '__all__'

#         exclude = {'credit_balance', }

#     def clean(self):
#         # print(self.instance.id)
#         data = self.cleaned_data
#         payment_type = data['payment_type']
#         payment_mode = data['payment_mode']
#         if (payment_type == 'PD' and payment_mode is not None) or (payment_type == 'NP' and payment_mode is not None):
#             raise forms.ValidationError(
#                 "A non-paying or paying debtor can't select mode of payment")
