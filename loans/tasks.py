from celery import shared_task
from .models import User

@shared_task
def calculate_credit_score(user_id):
    user = User.objects.get(id=user_id)
    # Fetch transactions from CSV and compute credit score (logic to be added)
    user.credit_score = 600  # Placeholder
    user.save()
