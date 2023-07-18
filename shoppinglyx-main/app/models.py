from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator,MinValueValidator
# Create your models here.
STATE_CHOICES =( 
    ('Andhra Pradesh','Andhra Pradesh'),
    ('Assam','Assam'),
    ('Arunachal Pradesh','Arunachal Pradesh'),
    ('Bihar','Bihar'),
    ('Chandigarh','Chandigarh'),
    ('Chattisgarh','Chattisgarh'),
    ('Daman & Diu','Daman & Diu'),
    ('Goa','Goa'),
    ('Gujarat','Gujarat'),
    ('Haryana','Haryana'),
    ('Himachal Pradesh','Himachal Pradesh'),
    ('Jammu kashmir','Jammu kashmir'),
    ('Jharkhand','Jharkhand'),
    ('Karanataka','Karanataka'),
    ('Rajasthan','Rajasthan'),
    ('Madhya Pradesh','Madhya Pradesh'),
    ('Uttar pradesh','Uttar pradesh'),
)

class Customer(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    locality = models.CharField(max_length=200)
    city = models.CharField(max_length=50)
    zipcode = models.IntegerField()
    state = models.CharField(choices=STATE_CHOICES,max_length=50)

    def __str__(self):
        return str(self.id)
    
CATEGORY_CHOICES = ( 
    ('P', 'Peda'),
    ('H', 'Halwa'),
    ('S', 'Shrikhand'),
    ('SF', 'Sugar Free'),
    ('DF', 'Dry Fruit'),
    ('BS', 'Bengali Sweets'),
    ('NS', 'Natural Sweets'),
)
class Product(models.Model):
    title = models.CharField(max_length=100)
    selling_price = models.FloatField()
    discounted_price = models.FloatField()
    description = models.TextField()
    category = models.CharField(choices=CATEGORY_CHOICES,max_length=2)
    product_image = models.ImageField(upload_to='productimg')

    def __str__(self):
        return str(self.id)

class Cart(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    product = models.ForeignKey(Product,on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)

    def __str__(self):
        return str(self.id)

    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price

STATUS_CHOICES = (
    ('Accepted','Accepted'),
    ('Packed','Packed'),
    ('On The Way','On The Way'),
    ('Delivered','Delivered'),
    ('Cancel','Cancel')
)

class Payment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.FloatField()
    razorpay_order_id = models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_status = models.CharField(max_length=100,blank=True,null=True)
    razorpay_payment_id = models.CharField(max_length=100,blank=True,null=True)
    paid = models.BooleanField(default=False)
    
class OrderPlaced(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    ordered_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=50,choices= STATUS_CHOICES,default='Pending')
    payment = models.ForeignKey(Payment,on_delete=models.CASCADE,default="")
    
    @property
    def total_cost(self):
        return self.quantity * self.product.discounted_price
'''
class Category(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name
    
class SubCategory(models.Model):
    name = models.CharField(max_length=200)
    category = models.ForeignKey(Category,on_delete=models.CASCADE)
    
    def __str__(self):
        return f"{self.category} - {self.name}"

'''
'''
class Review(models.Model):
    user = models.ForeignKey(User, models.CASCADE)
    product = models.ForeignKey(Product,models.CASCADE)
    comment = models.ForeignKey(Product, models.CASCADE)
    rate = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return str(self.id)'''