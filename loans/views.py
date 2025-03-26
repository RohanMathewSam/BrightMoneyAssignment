from decimal import Decimal
import json
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework import generics
from django.http import JsonResponse
from .models import User, Loan, Payment
from .serializers import UserSerializer, LoanSerializer, PaymentSerializer
from django.contrib import messages
import uuid  
from django.views.decorators.csrf import csrf_exempt

# API Views
class RegisterUserView(generics.CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class ApplyLoanView(generics.CreateAPIView):
    queryset = Loan.objects.all()
    serializer_class = LoanSerializer

class MakePaymentView(generics.CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer

# Rendered Views (HTML templates)
def home_view(request):
    return render(request, 'loans/index.html')

def register_view(request):
    if request.method == "POST":
        aadhar = request.POST['aadhar']
        name = request.POST['name']
        email = request.POST['email']
        annual_income = request.POST['income']

        # Handle user registration
        user = User.objects.create(
            aadhar_id=aadhar, name=name, email=email, annual_income=annual_income)
        user.save()

        messages.success(request, 'User registered successfully!')
        return redirect('home')

    return render(request, 'loans/register.html')
def apply_loan_view(request):
    if request.method == "POST":
        user_name = request.POST['user_name']  # ✅ Fetch user name

        # ✅ Get user using name
        user = get_object_or_404(User, name=user_name)

        # ✅ Convert input values to the correct types
        loan_amount = Decimal(request.POST['loan_amount'])  # Convert to Decimal
        interest_rate = Decimal(request.POST['interest_rate'])  # Convert to Decimal
        term_period = int(request.POST['term_period'])  # Convert to Integer

        # ✅ Create and save the loan
        loan = Loan.objects.create(
            user=user, loan_amount=loan_amount, interest_rate=interest_rate, term_period=term_period
        )
        loan.save()

        messages.success(request, 'Loan application submitted successfully!')
        return redirect('home')

    return render(request, 'loans/apply_loan.html')


def make_payment_view(request):
    if request.method == "POST":
        user_name = request.POST.get('user_name')  # ✅ Fetch user name

        # ✅ Get user using name
        user = get_object_or_404(User, name=user_name)

        # ✅ Fetch the loan using the user
        loan = get_object_or_404(Loan, user=user)

        # ✅ Fetch the stored `total_due`
        total_due = loan.total_due  # ✅ Use pre-calculated value

        # ✅ Convert amount from POST request to Decimal
        amount_paid = Decimal(request.POST['amount'])

        # ✅ Create a payment entry
        payment = Payment.objects.create(loan=loan, amount_paid=amount_paid)
        payment.save()

        # ✅ Mark the loan as "PAID" after payment
        loan.status = "PAID"
        loan.save()

        messages.success(request, 'Payment processed successfully! Loan is now marked as PAID.')
        return redirect('home')

    return render(request, 'loans/make_payment.html')

def get_statement(request):
    return render(request, 'loans/statement.html')

@csrf_exempt  # ❌ Remove in production
def get_statement_view(request):
    print("🔹 Request received at get_statement_view")

    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_name = data.get("user_name")  # ✅ Fetch user name from request
            print("📌 Received User Name:", user_name)

            if not user_name:
                return JsonResponse({"error": "User Name is required!"}, status=400)

            # ✅ Fetch the user
            user = get_object_or_404(User, name=user_name)

            # ✅ Fetch the Loan for this user
            loan = get_object_or_404(Loan, user=user)

            # ✅ Fetch all past transactions
            past_transactions = Payment.objects.filter(loan=loan).order_by("payment_date")

            # ✅ Convert past transactions to JSON (Ignore zero payments)
            past_transactions_data = [
                {"date": payment.payment_date.strftime("%Y-%m-%d"), "amount_paid": str(payment.amount_paid)}
                for payment in past_transactions if payment.amount_paid > 0  # ✅ Ignore ₹0.00 payments
            ]

            # ✅ Calculate remaining due amount
            total_paid = sum(payment.amount_paid for payment in past_transactions)
            remaining_due = loan.total_due - Decimal(total_paid)

            # ✅ Determine upcoming payments
            upcoming_transactions_data = []
            if remaining_due > 0:
                upcoming_transactions_data.append({"date": "2024-05-01", "amount_due": str(remaining_due)})

            return JsonResponse({
                "loan_id": str(loan.id),
                "loan_amount": str(loan.loan_amount),
                "interest_rate": loan.interest_rate,
                "term_period": loan.term_period,
                "status": loan.status,  # ✅ Add loan status
                "past_transactions": past_transactions_data,
                "upcoming_transactions": upcoming_transactions_data
            }, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data!"}, status=400)
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found!"}, status=404)
        except Loan.DoesNotExist:
            return JsonResponse({"error": "No active loans found for this user!"}, status=404)
        except Exception as e:
            return JsonResponse({"error": f"Unexpected error: {str(e)}"}, status=500)

    return JsonResponse({"error": "Invalid request method!"}, status=405)

@csrf_exempt
def fetch_loan_amount(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            user_name = data.get("user_name")

            if not user_name:
                return JsonResponse({"error": "User Name is required!"}, status=400)

            # ✅ Get user using name
            user = get_object_or_404(User, name=user_name)

            # ✅ Fetch the loan using the user
            loan = get_object_or_404(Loan, user=user)

            # ✅ Retrieve the stored `total_due` (Pre-calculated at loan creation)
            total_due = loan.total_due  # ✅ Use the stored value, no recalculation

            return JsonResponse({
                "loan_amount": str(loan.loan_amount),
                "interest_rate": loan.interest_rate,
                "term_period": loan.term_period,
                "total_due": str(total_due)  # ✅ Use pre-calculated value
            }, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"error": "Invalid JSON data!"}, status=400)
        except User.DoesNotExist:
            return JsonResponse({"error": "User not found!"}, status=404)
        except Loan.DoesNotExist:
            return JsonResponse({"error": "No active loans found for this user!"}, status=404)
        except Exception as e:
            return JsonResponse({"error": f"Unexpected error: {str(e)}"}, status=500)

    return JsonResponse({"error": "Invalid request method!"}, status=405)
