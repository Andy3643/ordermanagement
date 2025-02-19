from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from .models import Order
from .forms import RawOrderForm, ManualOrderForm
from datetime import date

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

    pending_orders = Order.objects.filter(is_done=False)
    completed_order_list = Order.objects.filter(is_done=True).order_by('-date_due')

    search_query = request.GET.get('search')
    if search_query:
        completed_order_list = completed_order_list.filter(order_name__icontains=search_query)

    paginator = Paginator(completed_order_list, 15)
    page_number = request.GET.get('page')
    completed_orders = paginator.get_page(page_number)

    return render(request, 'orders/order_list.html', {
        'raw_form': raw_form,
        'manual_form': manual_form,
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
