from django.shortcuts import render

from .models import ShippingAddress, Order, OrderItem

from cart.cart import Cart

from django.http import JsonResponse

def checkout(request):

    if request.user.is_authenticated:                                                                                   #users with accounts, (check if can prefill the form)

        try:                                                                                                            #check if authenticated user has shipping address

            shipping_address = ShippingAddress.objects.get(user=request.user.id)

            context ={'shipping':shipping_address}                                                                      #if the shipping address is found a dictionary is created
                                                                                                                        # a filled in form can be returned
            return render(request, 'payment/checkout.html', context=context)

        except:                                                                                                         #authenticated user without shipping address,
                                                                                                                        #needs to fill in the form
            return render(request, 'payment/checkout.html')

    else:                                                                                                               #guest user, needs to fill in the form

        return render(request, 'payment/checkout.html')



def complete_order(request):                                                                                            #handles the request coming from Ajax from checkout.html

    if request.POST.get('action') =='post':                                                                             #making sure that request from AJAX from checkout.html is a post

        name=request.POST.get('name')                                                                                   #retrieving specific data fields from AJAX function
        email=request.POST.get('email')

        address1 = request.POST.get('address1')
        address2 = request.POST.get('address2')
        city = request.POST.get('city')

        state = request.POST.get('state')
        postal_code = request.POST.get('postal_code')

        shipping_address = (address1 +"\n" + address2+"\n" + city+"\n"+ state+"\n"+postal_code)                         #styling user shipping address

        cart = Cart(request)                                                                                            #shopping cart info

        total_cost = cart.get_total()                                                                                   #using get total function from cart.py, assigning it to a value,
                                                                                                                        #amount_paid from models


                           # 1) Users with and without shipping info

        if request.user.is_authenticated:

            order = Order.objects.create(full_name=name,email=email,shipping_address=shipping_address,                  #full_name and amount_paid from model,
            amount_paid=total_cost, user=request.user)                                                                  #adding a user foreign key

            order_id = order.pk                                                                                         #primary key of order, order_id in the order_item

        # order_id used as a foreign key to connect the OrderItem model to the Order model

            for item in cart:

                OrderItem.objects.create(order_id=order_id, product=item['product'],quantity=item['qty'],               #as order cart items are being created, they are
                                                                                                                        #connected to a order model; 3 products = 3 order items
                price=item['price'], user=request.user)


                                #2) Guest Users

        else:

            order = Order.objects.create(full_name=name, email=email,shipping_address=shipping_address,                 # full_name and amount_paid from Order model
            amount_paid = total_cost)

            order_id = order.pk                                                                                         # primary key of order, order_id in the order_item



        #order_id used as a foreign key to connect the OrderItem model to the Order model

            for item in cart:
                OrderItem.objects.create(order_id=order_id, product=item['product'], quantity=item['qty'],              # as order cart items are being created, they are
                                                                                                                        # connected to a order model; 3 products = 3 order items
                price=item['price'])



        order_success = True

        response = JsonResponse({'success':order_success})                                                              #sent back to Ajax in checkout.html

        return response

def payment_success(request):                                                                                           #Clearing shopping cart once transaction has been completed

    for key in list(request.session.keys()):

        if key =='session_key':                                                                                         #key located in cart/cart/ class cart, cart

            del request.session[key]

    return render(request,'payment/payment-success.html')

def payment_failed(request):

    return render(request,'payment/payment-failed.html')
