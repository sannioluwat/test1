from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.mixins import (
    LoginRequiredMixin, PermissionRequiredMixin)
from django.contrib import messages
from django.urls import reverse_lazy, reverse
from django.views import generic
from .forms import ReservationForm
from reservations.models import Reservation
from . import models
from django.contrib.auth import get_user_model
from django.http import HttpResponseRedirect
from django.core.exceptions import ValidationError
from datetime import datetime, date, timedelta, time
from django.http import HttpResponse
from django.db.models import Q
from django.utils import timezone
from django.db.models import Sum
from django.db.models import F

# Create your views here.


class CreateReservation (LoginRequiredMixin, generic.CreateView):
    model = Reservation
    form_class = ReservationForm


class ListReservations(generic.ListView):
    model = Reservation

    # reserve should be included only for same day reservation
    criterion1 = Q(roomstatus__contains="reserve")

    criterion2 = Q(roomstatus__contains="checkin")
    today = datetime.now().date()
    criterion3 = Q(check_in__date__lte=today)
    criterion4 = Q(check_out__date__gte=today)

    def get_queryset(self):
        return Reservation.objects.filter(self.criterion3 & self.criterion4).filter(self.criterion1 | self.criterion2)


class CheckOutReservations(generic.ListView):
    context_object_name = 'check_out_list'

    def get_queryset(self):
        return Reservation.objects.filter(roomstatus__contains="checkout").order_by('-check_out')
    template_name = 'reservations/reservation_checkout.html'


class FutureReservations(generic.ListView):
    # model = Reservation
    # today = timezone.now().date()
    today = datetime.now().date()
    criterion1 = Q(roomstatus__contains="reserve")
    # criterion2 = Q(check_in__date__gt=today)

    context_object_name = 'future_list'

    # criterion1 = Q(roomstatus__contains="checkout")

    def get_queryset(self):
        return Reservation.objects.filter(self.criterion1).order_by('-check_in')
    template_name = 'reservations/reservation_future.html'


class NonPayingDebt(generic.ListView):
    # today = timezone.now().date()

    criterion1 = Q(roomstatus__contains="checkin")
    criterion2 = Q(roomstatus__contains="checkout")
    criterion3 = Q(payment_type__contains="NP")

    context_object_name = 'nonpaying_list'

    # criterion1 = Q(roomstatus__contains="checkout")

    def get_queryset(self):
        return Reservation.objects.filter(self.criterion1 | self.criterion2).filter(self.criterion3).order_by('-check_out')
    template_name = 'reservations/reservation_nonpaying.html'


class PayingDebt(generic.ListView):
    # today = timezone.now().date()

    criterion1 = Q(roomstatus__contains="checkin")
    criterion2 = Q(roomstatus__contains="checkout")
    criterion3 = Q(payment_type__contains="PD")

    context_object_name = 'payingdebtor_list'
    # criterion1 = Q(roomstatus__contains="checkout")

    def get_queryset(self):
        return Reservation.objects.filter(self.criterion1 | self.criterion2).filter(self.criterion3).order_by('-check_out')
    template_name = 'reservations/reservation_payingdebtor.html'


# class PPMT(generic.ListView):
#     # today = timezone.now().date()
#     today = datetime.now().date()

#     criterion1 = Q(book_date__date__lt=F(
#         'check_in__date'))  # or roomstatus = reserve
#     criterion5 = Q(payment_type__exact="P")
#     # extra criterion needs to be added--payment_type = P---Added
#     criterion2 = Q(book_date__date=today)
#     criterion3 = Q(total_cost__gt=F('room_price'))
#     criterion4 = Q(credit_balance__gt=0)
#     # Add 1 more filter--where available credit is true---Added.
#     context_object_name = 'ppmt_list'

#     def get_queryset(self):
#         return Reservation.objects.filter((self.criterion1 & self.criterion5) | (self.criterion2 & self.criterion3)).filter(self.criterion4)
#         # Add or to the filter for those who pay for multiple days
#         # or no_of_days > 1 and (current date >checkin and current date < checkout)
#     template_name = 'reservations/reservation_ppmt.html'


class LateCheckOut(generic.ListView):
    # today = timezone.now().date()

    # result = check_out + timedelta(hours=12)
    twelvepm = datetime.combine(
        date.today(),
        time(12, 1))

    criterion1 = Q(roomstatus__contains="checkin")
    criterion2 = Q(check_out__date=datetime.now().date())
    # criterion3 = Q(check_out__date=datetime.now().date())
    # print(datetime.now())
    # check_out_time = datetime.today().replace(
    #     hour=12, minute=0, second=0, microsecond=0)
    context_object_name = 'late_checkout'

    def get_queryset(self):
        if datetime.now() > self.twelvepm:
            return Reservation.objects.filter(self.criterion1).filter(self.criterion2).order_by('-check_out')
    template_name = 'reservations/reservation_latecheckut.html'


class AccountSummary(generic.ListView):

    today = datetime.now().date()

    twoam = datetime.combine(
        date.today(),
        time(2, 0))  # might have to include seconds so that it doesn't loop for a minute
    model = Reservation

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        # while self.twoam:
        # queryset = self.get_queryset()

        context['total_sales'] = Reservation.objects.filter(roomstatus__contains="checkin").aggregate(
            Sum('room_price')).get('room_price__sum')

        # Paying at checkin 1 day
        # exclude(check_in__lt=self.today) ensures that we collect the pay for multiple booking just once so that
        context['total_paying'] = Reservation.objects.filter(
            payment_type__exact="P").filter(paid_date=self.today).aggregate(Sum('total_cost')).get('total_cost__sum')

        context['total_paying_tf'] = Reservation.objects.filter(
            payment_mode__exact="TF").filter(paid_date=self.today).aggregate(Sum('total_cost')).get('total_cost__sum')

        context['total_paying_cash'] = Reservation.objects.filter(
            payment_mode__exact="C").filter(paid_date=self.today).aggregate(Sum('total_cost')).get('total_cost__sum')

        context['total_paying_pos'] = Reservation.objects.filter(
            payment_mode__exact="P").filter(paid_date=self.today).aggregate(Sum('total_cost')).get('total_cost__sum')
        # can we reserve debtors?if yes modify code
        context['total_non_paying'] = Reservation.objects.filter(roomstatus__contains="checkin").filter(
            payment_type__exact="NP").aggregate(Sum('total_cost')).get('total_cost__sum')
        context['total_paying_debtor'] = Reservation.objects.filter(roomstatus__contains="checkin").filter(
            payment_type__exact="PD").aggregate(Sum('total_cost')).get('total_cost__sum')

        # PPMT for future reservations
        # filter with roomstatus__contains="reserve" or book_date__date__lt=F('check_in__date' is fine
        # Also filter with book_date__date = current date (I should do date -1 because account is taken @ 2AM the following day)

        # context['total_paying_ppmt'] = Reservation.objects.filter(book_date__date__lt=F('check_in__date')).filter(
        #     payment_type__exact="P").filter(book_date__date=self.today).aggregate(Sum('total_cost')).get('room_price__sum')

        # context['total_paying_ppmt_tf'] = Reservation.objects.filter(book_date__date__lt=F('check_in__date')).filter(
        #     payment_mode__exact="TF").filter(book_date__date=self.today).aggregate(Sum('total_cost'))

        # context['total_paying_ppmt_cash'] = Reservation.objects.filter(book_date__date__lt=F('check_in__date')).filter(
        #     payment_mode__exact="C").filter(book_date__date=self.today).aggregate(Sum('total_cost'))
        # context['total_paying_ppmt_pos'] = Reservation.objects.filter(book_date__date__lt=F('check_in__date')).filter(
        #     payment_mode__exact="P").filter(book_date__date=self.today).aggregate(Sum('total_cost'))
        # total for guest using credit coming from reservations
        # we can add filter paypemt_type p to distinguish it from debtor reservations should management ask for it.
        # context['total_paying_with_credit'] = Reservation.objects.filter(roomstatus__contains="checkin").filter(
        #     book_date__date__lt=F('check_in__date')).filter(
        #     credit_balance__gt=0).aggregate(Sum('room_price'))
        # # ppmt for extra days of same day multiple bookings
        # context['total_paying_ppmt'] = Reservation.objects.filter(roomstatus__contains="checkin").filter(
        #     book_date__date=self.today).filter(total_cost__gt=F('room_price')).aggregate(Sum('room_price'))

        return context

    template_name = 'reservations/reservation_accsum.html'


class DetailReservation(generic.DetailView):
    model = Reservation


class UpdateReservation(LoginRequiredMixin, generic.UpdateView):
    login_url = '/login/'
    redirect_field_name = 'reservations/reservation_detail.html'

    form_class = ReservationForm

    model = Reservation

    # def form_valid(self, form):
    #     # self.object = form.save(commit=False)
    #     # self.object.user = self.request.user
    #     self.object.save()
    #     return super().form_valid(form)

# def reservation_update(request, pk):
#     reservation = get_object_or_404(Reservation, pk=pk)
#     # form = ReservationForm(instance=reservation)
#     # reservation_queryset = Reservation.objects.filter(pk=pk)
#     if request.method == 'POST':
#         form = ReservationForm(request.POST, instance=reservation)
#         if form.is_valid():
#             # check_in = name_form.cleaned_data['name']
#             # other_field = course_form.cleaned_data['other_field']
#             # form.update()
#             form.save()
#             return redirect('reservations')
#     else:
#         # print(form.errors)

#         form = ReservationForm(instance=reservation)
#     context = {
#         # 'name_form': name_form,
#         'form': form,
#     }
#     return render(request, 'reservations/reservation_update.html', context)


class DeleteReservation(LoginRequiredMixin, generic.DeleteView):
    model = models.Reservation
    # select_related = ("user", "group")
    success_url = reverse_lazy("reservations:all")

    # def get_queryset(self):
    #     queryset = super().get_queryset()
    #     return queryset.filter(user_id=self.request.user.id)

    def delete(self, *args, **kwargs):
        messages.success(self.request, "Reservation Deleted")
        return super().delete(*args, **kwargs)


#######################################
## Functions that require a pk match ##
#######################################


def cust_checkin(request, pk):
    reserve = get_object_or_404(Reservation, pk=pk)
    reserve.checkin()
    return redirect('reservations:all')


def cust_checkout(request, pk):
    reserve = get_object_or_404(Reservation, pk=pk)
    reserve.checkout()
    return redirect('reservations:all')

# def cust_checking_in_now(request, pk):
#     cust = get_object_or_404(Reservation, pk=pk)
#     cust.checking_in_now()
#     return redirect('reservations:all')


def testing(request):
    #   template = loader.get_template('reservation_list.html')
    context = {
        'mydate': datetime.now(),
    }
    return render(request, 'reservations/reservation_list.html', context)
