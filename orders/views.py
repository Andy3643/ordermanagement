from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import Order
from .forms import RawOrderForm, ManualOrderForm
from datetime import date, timedelta

def order_list(request):
    raw_form = RawOrderForm()
    manual_form = ManualOrderForm()

    if request.method == "POST":
        if 'raw_order_submit' in request.POST:
            raw_form = RawOrderForm(request.POST)
            if raw_form.is_valid():
                extracted_data = raw_form.cleaned_data.get("raw_order_input")
                Order.objects.create(**extracted_data)
                return redirect('order_list')

        elif 'manual_order_submit' in request.POST:
            manual_form = ManualOrderForm(request.POST)
            if manual_form.is_valid():
                manual_form.save()
                return redirect('order_list')

    today = date.today()
    tomorrow = today + timedelta(days=1)  # Get tomorrow's date

    # Get pending orders sorted in ascending order (earliest due date & time first)
    pending_orders = Order.objects.filter(is_done=False).order_by('date_due', 'time_due')

    # Get completed orders sorted by most recent first
    completed_orders = Order.objects.filter(is_done=True).order_by('-date_due', '-time_due')

    # Paginate completed orders (15 per page)
    paginator = Paginator(completed_orders, 15)
    page_number = request.GET.get('page')
    completed_orders_page = paginator.get_page(page_number)

    # Get orders due today
    orders_due_today = Order.objects.filter(date_due=today)
    total_orders_today = orders_due_today.count()

    # Get completed orders for today
    completed_today = orders_due_today.filter(is_done=True).count()

    # Calculate today's progress percentage
    progress_today = (completed_today / total_orders_today * 100) if total_orders_today > 0 else 0

    # Get orders from Monday to Sunday of this week
    start_of_week = today - timedelta(days=today.weekday())  # Monday of this week
    end_of_week = start_of_week + timedelta(days=6)  # Sunday of this week
    orders_this_week = Order.objects.filter(date_due__range=[start_of_week, end_of_week])
    total_orders_this_week = orders_this_week.count()

    # Get orders from last week (Monday - Sunday)
    start_of_last_week = start_of_week - timedelta(days=7)
    end_of_last_week = start_of_week - timedelta(days=1)
    orders_last_week = Order.objects.filter(date_due__range=[start_of_last_week, end_of_last_week])
    total_orders_last_week = orders_last_week.count()

    # Calculate % change in order volume
    if total_orders_last_week > 0:
        order_change_percentage = ((total_orders_this_week - total_orders_last_week) / total_orders_last_week) * 100
    else:
        order_change_percentage = 0  # No orders last week means no change calculation

    # Determine if the order change is positive or negative
    order_change_class = "positive" if order_change_percentage > 0 else "negative"

    # NEW: Get the total number of orders due tomorrow
    total_orders_tomorrow = Order.objects.filter(date_due=tomorrow).count()

    return render(request, 'orders/order_list.html', {
        'raw_form': raw_form,
        'manual_form': manual_form,
        'pending_orders': pending_orders,
        'completed_orders': completed_orders_page,
        'today': today,
        'total_orders_today': total_orders_today,
        'progress_today': round(progress_today, 2),  # Rounded to 2 decimal places
        'total_orders_this_week': total_orders_this_week,
        'order_change_percentage': round(order_change_percentage, 2),
        'order_change_class': order_change_class,
        'paginator': paginator,
        'total_orders_tomorrow': total_orders_tomorrow,  # Send tomorrow's order count to the template
    })



def mark_order_done(request, order_id):
    order = Order.objects.get(id=order_id)
    order.is_done = True
    order.save()
    return redirect('order_list')

def delete_order(request, order_id):
    order = Order.objects.get(id=order_id)
    order.delete()
    return redirect('order_list')
