from datetime import date


def check_preorders():
    from .models import PreOrder
    # Get today's date
    today = date.today()
    # Fetch preorders with the arrival date of today and status pending
    preorders = PreOrder.objects.filter(arrival_date=today, status='pending')
    for preorder in preorders:
        preorder.complete_order()
        print(f"PreOrder ID {preorder.id} marked as completed.")
