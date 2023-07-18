from django.shortcuts import render,redirect
from django.views import View
from .models import Customer, Product, Cart,OrderPlaced,Payment
from .forms import CustomerRegistrationForm,CustomerProfileForm
from django.contrib import messages
from django.db.models import Q,Count
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.shortcuts import render, redirect
from django.http import HttpResponse
from datetime import datetime
import razorpay
from django.conf import settings
#generate pdf
from io import BytesIO
from django.template.loader import get_template
from xhtml2pdf import pisa

class ProductView(View):
 def get(self,request):
  totalitem = 0
  peda = Product.objects.filter(category='P')
  halwa = Product.objects.filter(category='H')  
  shrikhand = Product.objects.filter(category='S')
  sugarfree = Product.objects.filter(category='SF')  
  dryfruit = Product.objects.filter(category='DF')
  bengalisweets = Product.objects.filter(category='BS')  
  naturalsweets = Product.objects.filter(category='NS')
  if request.user.is_authenticated:
    totalitem = len(Cart.objects.filter(user=request.user))
  return render(request,'app/home.html',{'peda':peda,'halwa':halwa,'shrikhand':shrikhand,'sugarfree':sugarfree,'dryfruit':dryfruit,'bengalisweets':bengalisweets,'naturalsweets':naturalsweets ,'totalitem':totalitem})


class ProductDetailView(View):
 def get(self,request,pk):
    totalitem = 0
    product = Product.objects.get(pk=pk)
    item_already_in_cart = False
    if request.user.is_authenticated:
      totalitem = len(Cart.objects.filter(user=request.user))
      item_already_in_cart = Cart.objects.filter(Q(product=product.id) & Q(user=request.user)).exists()
    return render(request,'app/productdetail.html',{'product':product,'item_already_in_cart':item_already_in_cart})

@login_required
def add_to_cart(request):
 user=request.user
 product_id = request.GET.get('prod_id')
 product = Product.objects.get(id=product_id)
 Cart(user=user, product=product).save()
 return redirect('/cart')

@login_required
def show_cart(request):
 if request.user.is_authenticated:
  user = request.user
  cart = Cart.objects.filter(user=user)
  #print(cart)
  amount = 0.0
  shipping_amount = 70.0
  total_amount = 0.0
  cart_product = [p for p in Cart.objects.all() if p.user == user]
  #print(cart_product)
  if cart_product:
   for p in cart_product:
    tempamount = (p.quantity * p.product.discounted_price)
    amount += tempamount
    totalamount = amount + shipping_amount
    return render(request,'app/addtocart.html',{'carts':cart,'totalamount':totalamount,'amount':amount})
  else:
    return render(request,'app/emptycart.html')
   
def plus_cart(request):
 if request.method == 'GET':
  prod_id = request.GET['prod_id']
  c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
  c.quantity+=1
  c.save()
  amount = 0.0
  shipping_amount = 70.0
  total_amount =0.0
  cart_product = [p for p in Cart.objects.all() if p.user == request.user]
  for p in cart_product:
    tempamount = (p.quantity * p.product.discounted_price)
    amount += tempamount

  data = {
     'quantity' : c.quantity,
     'amount' :amount,
     'totalamount':amount + shipping_amount
    }
  return JsonResponse(data)
   
def minus_cart(request):
 if request.method == 'GET':
  prod_id = request.GET['prod_id']
  c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
  c.quantity-=1
  c.save()
  amount = 0.0
  shipping_amount = 70.0
  total_amount =0.0
  cart_product = [p for p in Cart.objects.all() if p.user == request.user]
  for p in cart_product:
    tempamount = (p.quantity * p.product.discounted_price)
    amount += tempamount

  data = {
     'quantity' : c.quantity,
     'amount' :amount,
     'totalamount':amount+shipping_amount
    }
  return JsonResponse(data)   

def remove_cart(request):
 if request.method == 'GET':
  prod_id = request.GET['prod_id']
  c = Cart.objects.get(Q(product=prod_id) & Q(user=request.user))
  c.delete()
  amount = 0.0
  shipping_amount = 70.0
  cart_product = [p for p in Cart.objects.all() if p.user == request.user]
  for p in cart_product:
    tempamount = (p.quantity * p.product.discounted_price)
    amount += tempamount

  data = {
    'amount' :amount,
    'totalamount':amount + shipping_amount
    }
  return JsonResponse(data)   


def buy_now(request):
 return render(request, 'app/buynow.html')

@login_required
def address(request):
 add = Customer.objects.filter(user=request.user)
 return render(request, 'app/address.html',{'add':add,'active':'btn-primary'})

@login_required
def orders(request):
  op = OrderPlaced.objects.filter(user=request.user)
  return render(request, 'app/orders.html',{'order_placed':op})
'''
def mobile(request,data=None):
 if data == None:
  mobiles = Product.objects.filter(category='M')
 elif data == 'Redmi' or data == 'Samsung':
 elif data == 'below':
  mobiles = Product.objects.filter(category='M').filter(discounted_price__lt=10000)  
 elif data == 'above':
  mobiles = Product.objects.filter(category='M').filter(discounted_price__gt=10000)  
 return render(request, 'app/mobile.html',{'mobiles':mobiles})

'''
class CustomerRegistrationView(View):
 def get(self,request):
  form = CustomerRegistrationForm()
  return render(request,'app/customerregistration.html',{'form':form})
 def post(self,request):
  form = CustomerRegistrationForm(request.POST)
  if form.is_valid():
   messages.success(request, 'Congratualations!!! Registered Successfully')
   form.save()
  return render(request,'app/customerregistration.html',{'form':form})

@login_required
def checkout(request):  
  user = request.user
  add = Customer.objects.filter(user=user)
  cart_items = Cart.objects.filter(user=user)
  amount = 0.0
  shipping_amount = 70.0
  totalamount =0.0
  cart_product = [p for p in Cart.objects.all() if p.user == request.user]
  if cart_product:
    for p in cart_product:      
      tempamount = (p.quantity * p.product.discounted_price)
      amount += tempamount
    totalamount = amount + shipping_amount
    razoramount = int(totalamount * 100)
    client = razorpay.Client(auth=(settings.RAZOR_KEY_ID,settings.RAZOR_KEY_SECRET))
    data = { "amount":razoramount,"currency":"INR","receipt":"order_rcptid_12"}
    payment_response = client.order.create(data=data)
    print(payment_response)
    #{'id': 'order_LWkoCNPW93CFt6', 'entity': 'order', 'amount': 107000, 'amount_paid': 0, 'amount_due': 107000, 'currency': 'INR', 'receipt': 'order_rcptid_12', 'offer_id': None, 'status': 'created', 'attempts': 0, 'notes': [], 'created_at': 1679964946}
    order_id = payment_response['id']
    order_status = payment_response['status']
    if order_status == 'created':
          payment = Payment(
            user=user,
            amount=totalamount,
            razorpay_order_id=order_id,
            razorpay_payment_status = order_status
          )
          payment.save()
    return render(request, 'app/checkout.html',{'add':add,'totalamount':totalamount,'cart_items':cart_items})

@login_required
def payment_done(request):
 order_id=request.GET.get('order_id')
 payment_id=request.GET.get('payment_id')
 cust_id = request.GET.get('cust_id')
 user = request.user
 customer=Customer.objects.get(id=cust_id)
 payment=Payment.objects.get(razorpay_order_id=order_id)
 payment.paid = True
 payment.razorpay_payment_id = payment_id
 payment.save()
 cart = Cart.objects.filter(user=user)
 for c in cart:
  OrderPlaced(user=user,customer=customer,product=c.product,quantity=c.quantity,payment=payment).save()
  c.delete()
 return redirect("orders")

@method_decorator(login_required,name='dispatch')
class ProfileView(View):
  def get(self,request):
    form = CustomerProfileForm()
    return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})
  
  def post(self,request):
    form = CustomerProfileForm(request.POST)
    if form.is_valid():
        usr = request.user
        name = form.cleaned_data['name']
        locality = form.cleaned_data['locality']
        city = form.cleaned_data['city']
        state = form.cleaned_data['state']
        zipcode = form.cleaned_data['zipcode']
        reg = Customer(user=usr,name=name,locality=locality,city=city,state=state,zipcode=zipcode)
        reg.save()
        messages.success(request,'Congratualation!!Profile Updated Successfully')
    return render(request,'app/profile.html',{'form':form,'active':'btn-primary'})
  
  

#contact form 
'''def contact(request):
    if request.method == 'POST':
		  form = ContactForm(request.POST)
		  if form.is_valid():
			  subject = "Website Inquiry" 
        body = {
        'first_name': form.cleaned_data['first_name'], 
        'last_name': form.cleaned_data['last_name'], 
        'email': form.cleaned_data['email_address'], 
        'message':form.cleaned_data['message'], 
        }
        message = "\n".join(body.values())

        try:
          send_mail(subject, message, 'admin@example.com', ['admin@example.com']) 
        except BadHeaderError:
          return HttpResponse('Invalid header found.')
        return redirect ("main:homepage")
    form = ContactForm()
    return render(request, "app/contact.html", {'form':form})'''
    
'''def contact(request):
      if request.method == "POST":
    name = request.POST.get('name')
    email = request.POST.get('email')
    phone = request.POST.get('phone')
    desc = request.POST.get('desc')
    contact = Contact(name=name,email=email,phone=phone,desc=desc,date=datetime.today())
    contact.save()
  return render(request, 'app/contact.html')
'''

class CategoryView(View):
  def get(self,request,val):
    product = Product.objects.filter(category=val)
    title = Product.objects.filter(category=val).values('title')
    return render(request,'app/category.html',locals())
  

class CategoryTitle(View):
  def get(self,request,val):
    product = Product.objects.filter(title=val)
    title = Product.objects.filter(category=product[0].category).values('title')
    return render(request,'app/category.html',locals())
  
def about(request):
  return render(request,'app/about.html')

def contact(request):
  return render(request,'app/contact.html')



def render_to_pdf(template_src, context_dict={}):
    template = get_template(template_src)
    html = template.render(context_dict)
    result = BytesIO()
    pdf = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), result)
    if not pdf.err:
        return HttpResponse(result.getvalue(), content_type='application/pdf')
    return None
# Automaticly downloads to PDF file
class DownloadPDF(View):
    def get(self, request, *args, **kwargs):
        pdf = render_to_pdf('app/pdf_template.html')
        response = HttpResponse(pdf, content_type='application/pdf')
        filename = "Invoice_%s.pdf" % ("12341231")
        content = "attachment; filename='%s'" % (filename)
        response['Content-Disposition'] = content
        return response
      
# Opens up page as PDF
data ={
  "company" : "Murlidhar Sweets",
  "address" : "Shop No 23, Samarpan Arcade, Bopal Cross Road, Ring Road, Bopal, Ahmedabad, Gujarat 380058",
  "city" : "Bopal",
  "state" : "Gujarat",
  "zipcode" : "3800058",
  
  "phone": "+91 93458 67890",
  "email": "murlidhar@gmail.com",
}
class ViewPDF(View):
    def get(self, request, *args, **kwargs):
        product = Product.objects.all()
        pdf = render_to_pdf('app/product_report.html',{'product':product})
        return HttpResponse(pdf, content_type='application/pdf')

class ViewPDF1(View):
    def get(self, request, *args, **kwargs):
        order = OrderPlaced.objects.all()
        pdf = render_to_pdf('app/order_report.html',{'order':order})
        return HttpResponse(pdf, content_type='application/pdf')


class ViewPDF2(View):
    def get(self, request, *args, **kwargs):
        cart = Cart.objects.all()
        pdf = render_to_pdf('app/cart_report.html', {'cart': cart})
        return HttpResponse(pdf, content_type='application/pdf')

class ViewPDF3(View):
    def get(self, request, *args, **kwargs):
        customer = Customer.objects.all()
        pdf = render_to_pdf('app/profileview_report.html', {'customer':customer})
        return HttpResponse(pdf, content_type='application/pdf')



def Review_rate(request):
  if request.method == "GET":
    prod_id = request.GET.get('prod_id')
    product = Product.objects.get(id=prod_id)
    comment = request.GET.get('comment')
    rate = request.GET.get('rate')
    user = request.user
    Review(user=user,product=product,comment=comment,rate=rate).save()
    return redirect('product_detail',id=prod_id)