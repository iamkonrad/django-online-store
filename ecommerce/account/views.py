from django.shortcuts import render, redirect

from . forms import CreateUserForm, LoginForm, UpdateUserForm

from payment.forms import ShippingForm                                                                                  #pushing changes with a form
from payment.models import ShippingAddress, OrderItem                                                                   # queries on a model

from django.contrib.auth.models import User

from django.contrib.sites.shortcuts import get_current_site
from .token import user_tokenizer_generate

from django.template.loader import render_to_string
from django.utils.encoding import force_bytes,force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode                                              #decode and encode token generator


from django.contrib.auth.models import auth
from django.contrib.auth import authenticate

from django.contrib.auth.decorators import login_required

from django.contrib import messages                                                                                     #to show popup notifications

def register(request):                                                                                                  #registration process starts HERE, once done passed
                                                                                                                        #to email-verification.html
    form = CreateUserForm()

    if request.method =='POST':

        form = CreateUserForm(request.POST)

        if form.is_valid():

            user=form.save()

            user.is_active = False                                                                                      #by default newly registered accounts deactivated before verification

            user.save()

            current_site=get_current_site(request)

            subject = 'Account verification email'

            message = render_to_string('account/registration/email-verification.html',{                                 #adding token handling to email-verification, preparing
                                                                                                                        #to pass it into email-verification.html
                'user':user,
                'domain':current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token': user_tokenizer_generate.make_token(user),
            })

            user.email_user(subject=subject,message=message)


            return redirect('email-verification-sent')                                                                  #once a form gets submitted, redirection to emaiil-verification-sent


    context ={'form':form}                                                                                              #passing in the form inside a context


    return render(request,'account/registration/register.html',context=context)

def email_verification(request,uidb64,token):                                                                           #pulling id from urls

    unique_id = force_str(urlsafe_base64_decode(uidb64))                                                                      #decoding user id
    user = User.objects.get(pk=unique_id)


    #IN CASE OF SUCCESS                                                                                                 #if user clicked on verification link

    if user and user_tokenizer_generate.check_token(user,token):

        user.is_active = True                                                                                           #activating user's account

        user.save()

        return redirect('email-verification-success')

    #IN CASE OF FAILURE

    else:

        return redirect('email-verification-failed')


def email_verification_sent(request):

    return render(request,'account/registration/email-verification-sent.html')


def email_verification_success(request):

    return render(request,'account/registration/email-verification-success.html')



def email_verification_failed(request):

    return render(request,'account/registration/email-verification-failed.html')



def my_login(request):

    form = LoginForm()

    if request.method =='POST':

        form = LoginForm(request,data=request.POST)

        if form.is_valid():

            username=request.POST.get('username')
            password=request.POST.get('password')

            user = authenticate(request,username=username,password=password)

            if user is not None:

                auth.login(request, user)

                return redirect('dashboard')


    context = {'form':form}

    return render(request,'account/my-login.html',context=context)



def user_logout(request):

    try:
                                                                                                                        # clearing the session
        for key in list(request.session.keys()):

            if key == 'session_key':

                continue

            else:

                del request.session[key]                                                                                # clearing all the keys from the session except
                                                                                                                        # for the  session key

    except KeyError:

        pass


    messages.success(request, "Logout success")                                                                         #once a user logs out he will be redirected to store and                                                                                                                      #shown a messag
    return redirect("store")

@login_required(login_url='my-login')
def dashboard(request):

    return render(request,'account/dashboard.html')

@login_required(login_url='my-login')
def profile_management(request):

    #Updating user's username and email

    user_form = UpdateUserForm(instance=request.user)                                                                   #updating a specific instance of user


    if request.method =='POST':

        user_form=UpdateUserForm(request.POST,instance=request.user)                                                    #based on the currently signed in user

        if user_form.is_valid():

            user_form.save()

            messages.info(request, "Account updated")

            return redirect('dashboard')


    context ={'user_form':user_form}

    return render(request,'account/profile-management.html',context=context)



@login_required(login_url='my-login')
def delete_account(request):

    user = User.objects.get(id=request.user.id)

    if request.method =='POST':

        user.delete()


        messages.error(request, "Account deleted.")                                                                     #changed to error so the for loop in base.html behaves properly



        return redirect('store')                                                                                        #users redirected to store after account deletion

    return render(request,'account/delete-account.html')

#SHIPPING
@login_required(login_url='my-login')                                                                                   #only logged in users can access this
def manage_shipping(request):

    try:

        shipping =  ShippingAddress.objects.get(user=request.user.id)                                                   # checkng whether a logged in user has already entered
                                                                                                                        # shipping information, it's OPTIONAL to enter it

    except ShippingAddress.DoesNotExist:

        shipping = None                                                                                                 #user account no shipping info

    form = ShippingForm(instance=shipping)                                                                              #if there is info then the form gets prefilled, if there is none it does not

    if request.method =='POST':

        form = ShippingForm(request.POST, instance=shipping)                                                            #whenever someone fills a shipping form, posting the data if no shipping form
                                                                                                                        #associated with that user then create it, if it existed, then update it

        if form.is_valid():

            shipping_user =form.save(commit=False)                                                                      #assigning the user FK on the object

            shipping_user.user = request.user                                                                           #adding the fk

            shipping_user.save()

            return redirect('dashboard')                                                                                #if user updates the shipping information

    context = {'form':form}

    return render (request, 'account/manage-shipping.html', context=context)


@login_required(login_url='my-login')
def track_orders(request):

    try:

        orders=OrderItem.objects.filter(user=request.user)                                                              #fetching the orders associated with a user, user FK

        context = {'orders': orders}

        return render(request, 'account/track-orders.html', context=context)

    except:                                                                                                             #in case user has no orders

        return render(request, 'account/track-orders.html')
                                                                                                                        #context making the data available for the html template