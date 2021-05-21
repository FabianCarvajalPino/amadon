from django.shortcuts import render, redirect
from .models import Order, Product
from django.db.models import Count

def index(request):
    context = {
        "all_products": Product.objects.all()
    }
    return render(request, "store/index.html", context)

def checkout(request):
    product_id = int(request.POST['id'])
    product_data = Product.objects.get(id = product_id)
    quantity_from_form = int(request.POST["quantity"])
    price_from_form = float(product_data.price)
    total_charge = quantity_from_form * price_from_form

    print("Charging credit card...")
    Order.objects.create(quantity_ordered=quantity_from_form, total_price=total_charge)

    return redirect('/paid')


def paid(request):
    last_order = Order.objects.last()
    orders = Order.objects.all()
    total_orders = 0
    total_price = 0
    for order in orders:
        total_orders = total_orders + order.quantity_ordered
        total_price = total_price + order.total_price
    context = {
        'order': last_order,
        'total_orders': total_orders,
        'total_price': total_price
    }
    return render(request, "store/checkout.html", context)