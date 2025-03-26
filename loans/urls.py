from django.urls import path
from .views import fetch_loan_amount, get_statement, home_view, register_view, apply_loan_view, make_payment_view, get_statement_view

urlpatterns = [
    path('', home_view, name='home'),
    path('register/', register_view, name='register'),
    path('apply-loan/', apply_loan_view, name='apply-loan'),
    path('make-payment/', make_payment_view, name='make-payment'),
    path('get-statement/', get_statement, name='get-statement'),
    path('get-statement-view/', get_statement_view, name='get-statement-view'),
    path('fetch-loan-amount/', fetch_loan_amount, name='fetch-loan-amount'),
]
