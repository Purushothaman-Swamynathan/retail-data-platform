from django.shortcuts import render
from .models import Transaction
from django.db.models import Sum


def format_inr(amount):
    if amount is None:
        return "0.00"
    if amount >= 10000000:  # 1 Crore
        return f"{amount/10000000:.2f} Cr"
    elif amount >= 100000:  # 1 Lakh
        return f"{amount/100000:.2f} L"
    else:
        return f"{amount:,.2f}"


def dashboard_view(request):
    total_transactions = Transaction.objects.count()
    fraud_count = Transaction.objects.filter(fraud_flag=True).count()

    # ✅ FIX: Handle None + format
    revenue_raw = Transaction.objects.aggregate(Sum('amount'))['amount__sum']
    revenue = format_inr(revenue_raw)

    # ✅ FIX: format top customers
    top_customers_raw = (
        Transaction.objects.values('customer_id')
        .annotate(total_spent=Sum('amount'))
        .order_by('-total_spent')[:5]
    )

    top_customers = []
    for c in top_customers_raw:
        top_customers.append({
            'customer_id': c['customer_id'],
            'total_spent': format_inr(c['total_spent'])
        })

    context = {
        'total_transactions': total_transactions,
        'fraud_count': fraud_count,
        'revenue': revenue,
        'top_customers': top_customers,
    }

    return render(request, 'dashboard.html', context)