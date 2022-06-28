from django.db import models
from django.db.models import JSONField
from django.contrib.auth.models import AbstractUser
import uuid

# Create your models here.
    
class UserAccounts(AbstractUser):
    User_id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    Address = models.TextField(blank=True, null=True, default="")
    pincode = models.CharField(max_length=10, default=0, blank=True, null=True)
    District = models.CharField(max_length=30)
    State = models.CharField(max_length=30)
    Country = models.CharField(max_length=30)
    mobile_no = models.CharField(max_length=20)
    tags=JSONField(blank=True,default=dict)
    email_verification_token = models.CharField(max_length=255, null=True, blank=True)
    forgot_password_token = models.CharField(max_length=255, null=True, blank=True)
    otp_code = models.CharField(max_length=10, null=True, blank=True)
    is_email_Verified = models.BooleanField(default=False)
    is_phone_Verified = models.BooleanField(default=False)
    profile_image = models.ImageField(upload_to="users/", null=True)
    # username = None
    # EMAIL_FIELD = 'email'
    # REQUIRED_FIELDS = ['email']
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = []
    class Meta:
        db_table="UserAccounts"

class Cart(models.Model):
    User_id = models.UUIDField(default=uuid.uuid4, editable=False)
    Food_id = models.UUIDField(default=uuid.uuid4, editable=False)
    Added_time = models.DateTimeField(auto_now_add=True)
    # quantity = models.IntegerField()
    # rate = models.DecimalField(max_digits=11, decimal_places=2)
    class Meta:
        db_table = "Cart"

class Alert(models.Model):
    User_id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    search_name= models.CharField(max_length=255)
    search_date=models.DateField(auto_now_add=True)
    class Meta:
        db_table="Alert"

class Notifications(models.Model):
    notification_id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    user_id = models.UUIDField(default=uuid.uuid4, editable=False)
    username = models.CharField(max_length=255)
    message=models.TextField()
    order_id = models.CharField(max_length=200,blank=True,null=True)
    profile_image = models.ImageField(upload_to="notifications/", null=True)
    is_viewed = models.BooleanField(default=False)
    notification_date = models.DateTimeField(auto_now_add=True)
    class Meta:
        db_table="Notifications"

class FoodItems(models.Model):
    food_id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    food_name = models.CharField(max_length=40)
    food_image = models.ImageField(upload_to="foods/")
    food_rate_per_quantity = models.DecimalField(max_digits=25, decimal_places=2)
    food_available_total_quantity = models.IntegerField()
    food_total_quantity = models.IntegerField(default=0)
    food_old_price = models.DecimalField(max_digits=25, decimal_places=2, default=0, blank=True)
    food_description = models.TextField(null=True, blank=True)
    food_ingredients = models.TextField(null=True, blank=True)
    food_pros = models.CharField(max_length=255)
    food_category = models.CharField(max_length=25, default="snacks")
    currently_ordered_quantity = models.IntegerField()
    till_now_ordered_total_quantity = models.IntegerField()
    is_food_available = models.BooleanField(default=False)
    food_added_date = models.DateTimeField(auto_now_add=True)
    expiry_days_count=models.IntegerField(default=0)
    class Meta:
        db_table = "FoodItems"

def upload_path(instance,filename):
    return '/'.join(['qrcodes',str(instance.app_id),filename])

class Orders(models.Model):
    user_id = models.UUIDField(default=uuid.uuid4, editable=False)
    order_id = models.UUIDField(unique=True, default=uuid.uuid4, editable=False)
    order_list= JSONField(blank=False)
    total_price = models.DecimalField(max_digits=25, decimal_places=2)
    no_of_items = models.IntegerField(default=0)
    qrcode_image = models.ImageField(upload_to=upload_path, blank=True, default='')
    ordered_date = models.DateTimeField(auto_now_add=True)
    purchasing_date = models.DateTimeField()
    payment_successful = models.BooleanField(default=False)
    is_purchased = models.BooleanField(default=False)
    purchased_date = models.DateTimeField(null=True, blank=True)
    is_prepared = models.BooleanField(default=False)
    is_packed = models.BooleanField(default=False)
    is_available_confirm = models.BooleanField(default=False)
    handover_date = models.DateTimeField(null=True, blank=True)
    class Meta:
        db_table = "Orders"
