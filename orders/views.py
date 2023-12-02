from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import Order
from .forms import OrderForm
from datetime import date

def order_list(request):
    # Handle form submission
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('order_list')
    else:
        form = OrderForm()

    # Handle pending orders
    pending_orders = Order.objects.filter(is_done=False)

    # Handle completed orders with pagination
    completed_order_list = Order.objects.filter(is_done=True).order_by('-date_due')  # Ordering by date due
    
    # Handle search
    search_query = request.GET.get('search')
    if search_query:
        completed_order_list = completed_order_list.filter(order_name__icontains=search_query)

    paginator = Paginator(completed_order_list, 15)  # Show 15 orders per page
    page_number = request.GET.get('page')
    completed_orders = paginator.get_page(page_number)

    # Render the template with context
    return render(request, 'orders/order_list.html', {
        'form': form,
        'pending_orders': pending_orders,
        'completed_orders': completed_orders,
        'today': date.today()
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
