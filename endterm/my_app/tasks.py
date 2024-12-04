from celery import shared_task
from django.utils.timezone import now
from .models import PreOrder


@shared_task
def check_preorders():
    """Check all pending preorders and mark them as completed if arrival_date is today."""
    today = now().date()
    preorders = PreOrder.objects.filter(arrival_date=today, status='pending')
    for preorder in preorders:
        preorder.complete_order()
    return f"{len(preorders)} preorders completed."


@shared_task
def check_preorders():
    print("Задача check_preorders была вызвана.")
