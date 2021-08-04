from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from app.forms import Reset_pass ,Mysetpassword


urlpatterns = [
    path('', views.home),
    path('product-detail/<int:id>/', views.product_detail, name='product-detail'),
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/', views.show_cart, name='cart'),
    path('pluscart/', views.plus_cart, name='pluscart'),
    path('minuscart/', views.minus_cart, name='minuscart'),
    path('removecart/', views.remove_cart, name='removecart'),
    path('checkout/', views.checkout, name='checkout'),
    path('paymentdone/', views.payment_done, name='paymentdone'),
    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.profile, name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('changepassword/', views.change_password, name='changepassword'),
    path('topwear/', views.topwear, name='topwear'),
    path('topwear/<slug:data>/', views.topwear, name='topweardata'),
    path('bottomwear/', views.bottomwear, name='bottomwear'),
    path('bottomwear/<slug:data>/', views.bottomwear, name='bottomweardata'),
    path('mobile/', views.mobile, name='mobile'),
    path('mobile/<slug:data>/', views.mobile, name='mobiledata'),
    path('login/', views.signin, name='login'),
    path('registration/', views.signup, name='signup'),
    path("logout/",views.user_logout,name="logout"),
    path("search/",views.search,name="search"),
    path("editprofile/",views.editprofile,name="editprofile"),

    
    # userregistrationstarts
    path('password-reset/',auth_views.PasswordResetView.as_view(
        template_name='registration/password_reset.html',
    form_class=Reset_pass),name='reset'),
    path('password_reset/done/',auth_views.PasswordResetDoneView.as_view(
        template_name='registration/password_reset_done.html')
    ,name='password_reset_done'),
    path('reset/<uidb64>/<token>',auth_views.PasswordResetConfirmView.as_view(
        template_name='registration/password_reset_confirm.html',form_class=Mysetpassword)
    ,name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(
        template_name='registration/password_reset_complete.html')
    ,name='password_reset_complete'),
    #user registrationends
    #Signup Email Verification
    path('activate/<uidb64>/<token>/', views.activate, name='activate'),

]+ static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)

