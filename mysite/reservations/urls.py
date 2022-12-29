from django.urls import path
from . import views

app_name = 'reservations'

urlpatterns = [
    path('', views.ListReservations.as_view(), name="all"),
    path("new/", views.CreateReservation.as_view(), name="create"),
    path("reservation/<int:pk>/delete",
         views.DeleteReservation.as_view(), name="delete"),
    path("reservation/<int:pk>/detail",
         views.DetailReservation.as_view(), name="detail"),
    path("reservation/<int:pk>/edit", views.UpdateReservation.as_view(),
         name="update"),
    path('reservation/<int:pk>/checkin',
         views.cust_checkin, name="cust_checkin"),
    path('reservation/<int:pk>/checkout/',
         views.cust_checkout, name="cust_checkout"),
    path('checkedoutlist',
         views.CheckOutReservations.as_view(), name="checked-out"),
    path('checkedoutlist',
         views.FutureReservations.as_view(), name="future_reserve"),
    path('nonpaying',
         views.NonPayingDebt.as_view(), name="nonpaying"),
    path('payingdebtor',
         views.PayingDebt.as_view(), name="payingdebt"),
    path('latecheckout',
         views.LateCheckOut.as_view(), name="late-checkout"),
    path('account-summary',
         views.AccountSummary.as_view(), name="acc-summary"),
    #     path('p-p-m-t',
    #          views.PPMT.as_view(), name="ppmt"),


]
