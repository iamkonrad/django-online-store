from django.shortcuts import render

from .models import ShippingAddress

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

    pass




def payment_success(request):

    return render(request,'payment/payment-success.html')

def payment_failed(request):

    return render(request,'payment/payment-failed.html')
