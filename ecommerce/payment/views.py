from django.shortcuts import render

def checkout(request):

    return render(request, 'payment/checkout.html')

def payment_success(request):

    return render(request,'payment/payment-success.html')

def payment_failed(request):

    return render(request,'payment/payment-failed.html')
