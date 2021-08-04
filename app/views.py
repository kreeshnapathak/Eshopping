from django.contrib.auth import authenticate, login, logout, update_session_auth_hash
from django.contrib.auth.models import User
from django.http import request
from django.http.response import HttpResponseRedirect, JsonResponse
from .models import Product,Customer, Cart,OrderPlaced
from django.shortcuts import redirect, render
from .forms import user_signup, loginform, Change_password, CustomerProfile,Userupdateform
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q

#for email Sign up email verifiction
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .token import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage


def home(request):
    totalitem=0
    topwears = Product.objects.filter(category = 'TW')
    buttomwears = Product.objects.filter(category = 'BW')
    mobiles = Product.objects.filter(category = 'M')
    if request.user.is_authenticated:
        totalitem= len(Cart.objects.filter(user=request.user))

        return render(request, 'app/home.html',{'topwears':topwears,'buttomwears': buttomwears, 'mobiles': mobiles, 'totalitems':totalitem})
    else:
        return render(request, 'app/home.html',{'topwears':topwears,'buttomwears': buttomwears, 'mobiles': mobiles})

def product_detail(request, id):
    totalitem=0
    # products = Product.objects.all()
    products = Product.objects.get(pk=id)
    if request.user.is_authenticated:
        
        totalitem= len(Cart.objects.filter(user=request.user))
        return render(request, 'app/productdetail.html',{'product':products, 'totalitems':totalitem})

    else:
        return render(request, 'app/productdetail.html',{'product':products})

#save cart data in database table Cart
def add_to_cart(request):
    if request.user.is_authenticated:
        user=request.user
        product_id=request.GET.get('prod_id')
        product= Product.objects.get(id=product_id)
        Cart(user=user,product=product).save()
        return redirect('/cart/')
    else:
        return redirect('/login')



#show and proceed data in Cart
@login_required
def show_cart(request):
    user=request.user
    cart=Cart.objects.filter(user=user)
    amount=0.0
    shipping_amount=70.0
    total_amount=0.0
    cart_product=[p for p in Cart.objects.all() if p.user==user]
    if cart_product:
        for p in cart_product:
            tempamount=(p.quantity * p.product.discounted_price)
            amount += tempamount
            total_amount = amount + shipping_amount
        return render (request, 'app/addtocart.html',{'carts':cart, 
            'totalamount':total_amount,'amount':amount})
    else:
        return render(request,'app/aemptycart.html')

def plus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c= Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity += 1
        c.save()
        amount=0.0
        shipping_amount=70.0
        cart_product=[p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
            tempamount=(p.quantity * p.product.discounted_price)
            amount += tempamount
            totalamount = amount 
        
        data = {
            'quantity':c.quantity,
            'amount': amount,
            'totalamount': totalamount+ shipping_amount
        }
        return JsonResponse(data)            

def minus_cart(request):
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c= Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.quantity -= 1
        c.save()
        amount=0.0
        shipping_amount=70.0
        cart_product=[p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
            tempamount=(p.quantity * p.product.discounted_price)
            amount += tempamount
            totalamount = amount 
        
        data = {
            'quantity':c.quantity,
            'amount': amount,
            'totalamount': totalamount+ shipping_amount
        }
        return JsonResponse(data)            

def remove_cart(request):
    cart_product=[p for p in Cart.objects.all() if p.user==request.user]
    if request.method == 'GET':
        prod_id = request.GET['prod_id']
        c= Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
        c.delete()
        amount=0.0
        shipping_amount=70.0
        cart_product=[p for p in Cart.objects.all() if p.user==request.user]
        for p in cart_product:
            tempamount=(p.quantity * p.product.discounted_price)
            amount += tempamount
        totalamount = amount 
        
        data = {
            'amount': amount,
            'totalamount': totalamount+ shipping_amount
        }
        return JsonResponse(data)            



def buy_now(request):
 return render(request, 'app/buynow.html')

@login_required
def profile(request):
    op= OrderPlaced.objects.filter(user=request.user).order_by("-ordered_date")[:5]
    totalorders=len(OrderPlaced.objects.filter(user=request.user))
    td=len(OrderPlaced.objects.filter(user=request.user).filter(status='Delivered'))
    pd=len(OrderPlaced.objects.filter(user=request.user).filter(status='Pending'))
    return render(request, 'app/profile.html',{'order_placed':op,'totalorders':totalorders,'td':td,'pd':pd,'active':'btn-primary'})
    
@login_required
def editprofile(request):
    if request.method == 'POST':
        uform = Userupdateform(request.POST,instance = request.user)
        cform = CustomerProfile(request.POST,instance = request.user.customer)
        if uform.is_valid() and cform.is_valid():
            messages.success(request, 'Password updated successfully!')
            uform.save()
            cform.save()
            return redirect('/editprofile/')
    else:     
        uform = Userupdateform(instance = request.user)
        cform = CustomerProfile(instance = request.user.customer)
    return render(request, 'app/editprofile.html',{'uform':uform,'cform':cform, 'active':'btn-primary'})


def address(request):
 return render(request, 'app/address.html',{'active':'btn-primary'})


@login_required
def change_password(request):
    if request.user.is_authenticated:
        if request.method == 'POST':
            form=Change_password(user=request.user, data=request.POST)
            if form.is_valid():
                messages.success(request, 'Password changed successfully!')
                form.save()
                update_session_auth_hash(request,form.user)
                return HttpResponseRedirect('/changepassword/')

        else:
            form  = Change_password(user=request.user)
    
        return render(request, 'app/changepassword.html',{'form':form,'active':'btn-primary'})
    
    else:
        return HttpResponseRedirect('/changepassword/')

def mobile(request, data = None):
    if data == None:
        mobiles = Product.objects.filter(category = 'M')
    elif data == 'Apple' or data == 'One Plus' or data == 'MI':
        mobiles = Product.objects.filter(category = 'M').filter(brand=data)
    elif data == 'below':
        mobiles = Product.objects.filter(category = 'M').filter(discounted_price__lt=70000)    
    elif data == 'above':
        mobiles = Product.objects.filter(category = 'M').filter(discounted_price__gt=100000)

    return render(request, 'app/mobile.html',{'products':mobiles})

def topwear(request, data = None):
    if data == None:
        topwear = Product.objects.filter(category = 'TW')
    elif data == 'Gurkhas' or data == 'MadeInNepal' or data == 'Zara':
        topwear = Product.objects.filter(category = 'TW').filter(brand=data)
    elif data == 'below':
        topwear = Product.objects.filter(category = 'TW').filter(discounted_price__lt=2000)    
    elif data == 'above':
        topwear = Product.objects.filter(category = 'TW').filter(discounted_price__gt=2000)

    return render(request, 'app/topwear.html',{'products':topwear})

def bottomwear(request, data = None):
    if data == None:
        bottomwear = Product.objects.filter(category = 'BW')
    elif data == 'Adidas' or data == 'Gurkhas' or data == 'Zara' or data == 'MadeInNepal' or data == 'Nike':
        bottomwear = Product.objects.filter(category = 'BW').filter(brand=data)
    elif data == 'below':
        bottomwear = Product.objects.filter(category = 'BW').filter(discounted_price__lt=2000)    
    elif data == 'above':
        bottomwear = Product.objects.filter(category = 'BW').filter(discounted_price__gt=2000)

    return render(request, 'app/bottomwear.html',{'products':bottomwear})


def signin(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = loginform(request = request, data = request.POST)
            if form.is_valid():
                uname = form.cleaned_data['username']
                upass = form.cleaned_data['password']
                user = authenticate(username = uname , password = upass)
                if user is not None:
                    login(request, user)
                    messages.success(request, 'Logged In')
                    return HttpResponseRedirect('/profile/')
        else:
            form = loginform()
        return render(request, 'app/login.html',{'form':form})
    else:
        return HttpResponseRedirect('/profile/')



def signup(request):
    if request.method == 'POST':
        form = user_signup(request.POST)
        cform = CustomerProfile(request.POST)
        if form.is_valid() and cform.is_valid:
            user = form.save(commit=False)
            cform.instance.user = user
            messages.success(request,"Congratulation! Your account has been created.")
            user.is_active = False
            user.save()
            cform.save()
            current_site = get_current_site(request)
            mail_subject = 'Activate your blog account.'
            message = render_to_string('registration/acc_active_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': force_text(urlsafe_base64_encode(force_bytes(user.pk))),
                'token':account_activation_token.make_token(user),
            })
            to_email = form.cleaned_data.get('email')
            email = EmailMessage(
                        mail_subject, message, to=[to_email]
            )
            email.send()
            return render(request, 'registration/activate_your_account.html')
    else:
        form = user_signup()
        cform = CustomerProfile()
    return render(request, 'app/signup.html', {'form': form,'cform':cform})



def activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        # return redirect('home')
        return render(request, 'registration/account_activate_success.html')
    else:
        return HttpResponse('Activation link is invalid!')




def user_logout(request):
    logout(request)
    return HttpResponseRedirect('/login/')


def checkout(request):
    user = request.user
    add = Customer.objects.filter(user = user)
    cart_items=Cart.objects.filter(user=user)
    amount = 0.0
    shippint_amount = 70.0
    totalamount = 0.0
    cart_product=[p for p in Cart.objects.all() if p.user == request.user]
    if cart_product:
        for p in cart_product:
            tempamount= (p.quantity * p.product.discounted_price)
            amount += tempamount
        totalamount= amount+shippint_amount    
    
    return render(request, 'app/checkout.html',{'details':add,'totalamount':totalamount,'cartitems':cart_items})


def payment_done(request):
    user= request.user
    # custid= request.Get.get('custid')
    customer= Customer.objects.get(user=user)
    cart= Cart.objects.filter(user=user)
    for c in cart:
        OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity).save()
        c.delete()
    
    return redirect('orders')

def orders(request):
    op= OrderPlaced.objects.filter(user=request.user).order_by("-ordered_date")
    return render(request, 'app/orders.html',{'order_placed':op,'active':'btn-primary'})
    


def search(request):
    query=request.GET['query']
    if len(query)<3:
        return HttpResponseRedirect("/")         
    else:    
        reasult=Product.objects.filter(Q(title__icontains=query) | Q(brand__icontains=query)  )
        
        return render(request,'app/search.html',{'reasult':reasult,'query':query})
    