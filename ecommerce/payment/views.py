from django.shortcuts import render

from .models import ShippingAddress, Order, OrderItem

from cart.cart import Cart

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



def complete_order(request):

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

        ''' Order variations:
        1) Users with and without shipping info
        2) Guest Users
        
        '''
def payment_success(request):

    return render(request,'payment/payment-success.html')

def payment_failed(request):

    return render(request,'payment/payment-failed.html')
