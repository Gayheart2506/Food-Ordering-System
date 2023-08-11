from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect
from django.http.response import JsonResponse
from django.contrib import messages
from django.urls import reverse
from .models import *
import datetime
from datetime import timedelta
from django.utils import timezone
import random

# Create your views here.
def dashboard(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    lunch = Food_Category.objects.get(category_name="Lunch")
    lunch_items = Food_Item.objects.filter(food_category=lunch)[:3]
    order = Order.objects.filter(user=request.user)

    return render(request, "dashboard/dashboard.html", {
        "lunchs": lunch_items,
        'order': order,
    })

def order(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    now = datetime.datetime.now()
    today_date = f"{now.day}/ {now.month}/ {now.year}"
    order = Order.objects.filter(user=request.user)
    ordersitems = OrderItem.objects.filter(order__user=request.user)
    return render(request, "dashboard/orders.html", {
        'orders': ordersitems, 
        'today_date': today_date,
    })

def foods(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    breakfast = Food_Category.objects.get(category_name="Breakfast")
    breakfast_items = Food_Item.objects.filter(food_category=breakfast)
    lunch = Food_Category.objects.get(category_name="Lunch")
    lunch_items = Food_Item.objects.filter(food_category=lunch)
    snack = Food_Category.objects.get(category_name="Snacks")
    snack_items = Food_Item.objects.filter(food_category=snack)

    return render(request, "dashboard/foods.html", {
        "breakfasts": breakfast_items,
        "lunchs": lunch_items,
        "snacks": snack_items
    })

def food_details(request, food_id):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    food = Food_Item.objects.get(pk=food_id)
    return render(request, "dashboard/food-details.html", {
        "food": food,
    })


def receipt(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    
    orders = Order.objects.filter(user=request.user)
    orders_items = OrderItem.objects.filter(order__in=orders)

    # Create a list to store the receipt details
    # receipts = []

    for order in orders:
        total_price = sum(item.food_item.Price * item.quantity for item in orders_items if item.order == order)
        orderss = Order.objects.filter(user=request.user)
        orders_itemss = OrderItem.objects.filter(order__in=orderss)
        # Get the time difference between the order date and the current date
        # time_diff = timezone.now() - order.created_at

        # if time_diff.days == 0:
            # If the order was placed today, use "Today" for the receipt date
            # receipt_date = "Today"
        # elif time_diff.days == 1:
            # If the order was placed yesterday, use "Yesterday" for the receipt date
            # receipt_date = "Yesterday"
        # else:
            # For orders older than yesterday, use the actual order date
            # receipt_date = order.created_at.strftime("%d/%m/%Y")

        # Calculate the total price for each order
       

        # Append the receipt details to the list
        # receipts.append({
        #     'order': order,
        #     'receipt_date': receipt_date,
        #     'total_price': total_price,
        #     'order_items': orders_itemss,
        # })

    return render(request, "dashboard/receipts.html", {
        # 'receipt_date': receipt_date,
        'total_price': total_price,
        'order_items': orders_itemss,
    })


def add_to_cart(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    if request.method == 'POST':
        if request.user.is_authenticated:
            food_id = int(request.POST.get('id'))
            food_qty = int(request.POST.get('qty'))

            food_item = get_object_or_404(Food_Item, pk=food_id)

            if food_item.quantity >= food_qty:
                # Check if the item is already in the user's cart
                cart_item, created = Cart.objects.get_or_create(user=request.user, food_item=food_item)

                if not created:
                    cart_item.food_qty += food_qty
                else:
                    cart_item.food_qty = food_qty

                cart_item.save()

                return JsonResponse({'status': 'success', 'message': 'Product added to cart'})
                
            else:
                return JsonResponse({'status': 'error', 'message': f'Only {food_item.quantity} quantity available'})
        else:
            return JsonResponse({'status': 'error', 'message': 'Login to continue'})

    return JsonResponse({'status': 'error', 'message': 'Invalid method: Only POST requests allowed for adding to cart'})


def cart(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    cart = Cart.objects.filter(user=request.user)
    total_price = 0
    for things in cart:
        total_price = total_price + things.food_item.Price * things.food_qty
    return render(request, "dashboard/cart.html", {
        'cart': cart,
        'total': total_price,
    })


def remove_item(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    if request.method == 'POST':
        food_id = request.POST.get('food_id')
        if Cart.objects.filter(user=request.user, food_item_id=food_id):
            cart_item = Cart.objects.get(food_item_id=food_id, user=request.user)
            cart_item.delete()
        return JsonResponse({'status': "deleted successfully !"})
    return redirect('dashboard')

def checkout(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    cart = Cart.objects.filter(user=request.user)
    total_price = 0
    for things in cart:
        total_price = total_price + things.food_item.Price * things.food_qty
    return render(request, "dashboard/checkout.html", {
        'cart': cart, 
        'total_price': total_price,
    })


def placeorder(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    if request.method == "POST":
        neworder = Order()
        neworder.user = request.user
        neworder.fname = request.POST.get('fname')
        neworder.lname = request.POST.get('lname')
        neworder.email = request.POST.get('email')
        neworder.phone = request.POST.get('phone')
        neworder.foodcat = request.POST.get('food_cat')
        neworder.message = request.POST.get('more_info')

        neworder.payment_mode = request.POST.get('payment_mode')

        cart = Cart.objects.filter(user=request.user)
        cart_total_price = 0

        for item in cart:
            cart_total_price = cart_total_price + item.food_item.Price * item.food_qty

        neworder.total_price = cart_total_price
        trackno = 'CU' + str(random.randint(1111111, 9999999))
        while Order.objects.filter(tracking_no=trackno) is None:
            trackno = 'CU' + str(random.randint(1111111, 9999999))
        
        neworder.tracking_no = trackno
        neworder.save()

        neworderitems = Cart.objects.filter(user=request.user)
        for item in neworderitems:
            OrderItem.objects.create(
                order=neworder,
                food_item=item.food_item,
                price = item.food_item.Price,
                quantity = item.food_qty
            )

            # To decrease the product quantity from available stock 

            orderfood = Food_Item.objects.filter(id=item.food_item_id).first()
            orderfood.quantity = orderfood.quantity - item.food_qty
            orderfood.save()

            # To clear users cart 

        Cart.objects.filter(user=request.user).delete()

        messages.success(request, "Your Order was successfull")

    return redirect('dashboard')

def proceed_to_pay(request):
    if not request.user.is_authenticated:
        return HttpResponseRedirect(reverse("login"))
    cart = Cart.objects.filter(user=request.user)
    total_price = 0
    for item in cart:
        total_price = total_price + item.food_item.Price * item.food_qty

    return JsonResponse({
        'total_price': total_price
    })


def receipt_info(request, receipts_id):
    order = Order.objects.filter(pk=receipts_id).filter(user=request.user).first()
    order_item = OrderItem.objects.filter(order=order)

    collection_time = order.created_at + timedelta(minutes=10)

    return render(request, "dashboard/receipt-info.html", {
        'order':order,
        'order_details': order_item,
        'collection_time': collection_time,

    })
