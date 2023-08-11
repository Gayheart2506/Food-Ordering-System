from django.urls import path
from . import views

urlpatterns = [
    path("", views.dashboard, name="dashboard"),
    path("Food/<int:food_id>", views.food_details, name="food_details"),
    path("orders", views.order, name="orders"),
    path("daily foods", views.foods, name="dailyfoods"),
    path("receipt", views.receipt, name="receipts"),
    path("add-to-cart", views.add_to_cart, name="addtocart"),
    path('food-cart', views.cart, name='cart'),
    path('remove-item', views.remove_item, name="removeitem"),
    path('check-out', views.checkout, name='checkout'),
    path('place-order', views.placeorder, name="placeorder"), 
    path("proceed-to-pay", views.proceed_to_pay, name="proceedtopay"),
    path("full-receipt-details/<int:receipts_id>", views.receipt_info, name="receipts_info"),

]