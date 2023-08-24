from django.shortcuts import render, redirect
from .models import Order
from .forms import OrderForm

def order_list(request):
    # If form is submitted
    if request.method == "POST":
        form = OrderForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('order_list')
    
    # If viewing the page
    else:
        form = OrderForm()
    
    pending_orders = Order.objects.filter(is_done=False)
    completed_orders = Order.objects.filter(is_done=True)
    
    return render(request, 'orders/order_list.html', {
        'form': form,
        'pending_orders': pending_orders,
        'completed_orders': completed_orders
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
