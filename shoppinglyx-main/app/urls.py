from django.urls import path
from app import views
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from .forms import LoginForm,MyPasswordChangeForm,MyPasswordResetForm,MySetPasswordForm


urlpatterns = [
    path('',views.ProductView.as_view(),name='home'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
 
    path('product-detail/<int:pk>',views.ProductDetailView.as_view(),name='product-detail'),
   
    path('add-to-cart/', views.add_to_cart, name='add-to-cart'),
    path('cart/',views.show_cart,name='showcart'),
    path('pluscart/',views.plus_cart),
    path('minuscart/',views.minus_cart),
    path('removecart/',views.remove_cart),

    path('buy/', views.buy_now, name='buy-now'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('address/', views.address, name='address'),
    path('orders/', views.orders, name='orders'),
    path('checkout/', views.checkout, name='checkout'),
    #path('checkout/', views.checkout.as_view(), name='checkout'),

    path('paymentdone/', views.payment_done, name='paymentdone'),
    
    path('accounts/login/',auth_views.LoginView.as_view(template_name='app/login.html',authentication_form=LoginForm),name='login'),
   
    #login and passwords 
    path('logout/',auth_views.LogoutView.as_view(next_page='login'),name='logout'),
    path('passwordchange/',auth_views.PasswordChangeView.as_view(template_name='app/passwordchange.html',form_class=MyPasswordChangeForm,success_url='/passwordchangedone/'),name='passwordchange'),
    path('passwordchangedone/',auth_views.PasswordChangeView.as_view(template_name='app/passwordchangedone.html'),name='passwordchangedone'),
    path('password-reset/',auth_views.PasswordResetView.as_view(template_name='app/password_reset.html',form_class=MyPasswordResetForm),name='password_reset'),
    path('password-reset/done/',auth_views.PasswordResetDoneView.as_view(template_name='app/password_reset_done.html'),name='password_reset_done'),
    path('password-reset-confirm/<uidb64>/<token>/',auth_views.PasswordResetConfirmView.as_view(template_name='app/password_reset_confirm.html',form_class=MySetPasswordForm),name='password_reset_confirm'),
    path('password-reset-complete/',auth_views.PasswordResetCompleteView.as_view(template_name='app/password_reset_complete.html'),name='password_reset_complete'),
    path('registration/',views.CustomerRegistrationView.as_view(),name="customerregistration"),

    path('category/<slug:val>',views.CategoryView.as_view(),name='category'),
    path('category-title/<val>',views.CategoryTitle.as_view(),name='category-title'),
    
    
    path('product_report/',views.ViewPDF.as_view(),name='product_report'),
    #path('checkout_report/',views.ViewPDF2.as_view(),name='checkout_report'),
    path('profileview_report/',views.ViewPDF3.as_view(),name='profileview_report'),
    path('order_report/',views.ViewPDF1.as_view(),name='order_report'),    
    path('cart_report/',views.ViewPDF2.as_view(),name='cart_report'),    
  
   #path('review/',views.Review_rate,name='review'),
]+ static(settings.MEDIA_URL,document_root=settings.MEDIA_ROOT)
