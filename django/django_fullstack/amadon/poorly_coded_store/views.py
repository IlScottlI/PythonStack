from django.shortcuts import render, redirect
from .models import Order, Product


def index(request):
    context = {
        "all_products": Product.objects.all()
    }
    return render(request, "store/index.html", context)


def checkout(request):
    try:
        context = request.session['context']
    except:
        context = {}
    return render(request, "store/checkout.html", context)


def process(request):
    action = redirect('/')
    try:
        type_ = request.POST['type']
    except:
        type_ = ''

    if type_ == 'new':
        quantity_from_form = int(request.POST["quantity"])
        price_from_db = float(Product.objects.get(
            id=request.POST["price_id"]).price)
        total_charge = quantity_from_form * price_from_db
        print("Charging credit card...")
        Order.objects.create(quantity_ordered=quantity_from_form,
                             total_price=total_charge)
        all_orders = Order.objects.all()
        all_orders_sum = 0
        total_items_ordered = 0
        for item in all_orders:
            total_items_ordered = total_items_ordered + item.quantity_ordered
            all_orders_sum = all_orders_sum + item.total_price
        context = {
            'total_charge': float(total_charge),
            'price_from_form': float(price_from_db),
            'quantity_from_form': float(quantity_from_form),
            'all_orders_sum': float(all_orders_sum),
            'total_items_ordered': total_items_ordered,
        }
        print(context)
        request.session['context'] = context
        action = redirect("/checkout", context)

    return action
