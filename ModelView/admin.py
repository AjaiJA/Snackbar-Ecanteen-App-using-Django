# from django.contrib import admin
from django.http.response import JsonResponse
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.db.models import Max, Count, Sum
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.contrib.sessions.models import Session
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.core.mail import EmailMessage
from django.contrib import messages
from ModelView.views import foodDetails
from .utils import account_activation_token
from django.urls import reverse
from django.views import View
from django.contrib import auth
from .models import Cart, UserAccounts, FoodItems, Orders
import base64, json
from django.core.files.base import ContentFile

# Register your models here.
    
def adminPanel(request):
    if request.user.is_authenticated:
        user = auth.get_user(request)
        if(user.username == "snackbar"):
            orders = Orders.objects.all()
            food_items = FoodItems.objects.all()
            items_count = food_items.count()
            order_count = orders.count()
            customer = UserAccounts.objects.all()
            customer_count = customer.count()
            progress_count = Orders.objects.filter(is_purchased=False).count()
            form = Orders()
            context = {
                'form': form,
                'orders': orders,
                'food_items': food_items,
                'items_count': items_count,
                'order_count': order_count,
                'customer_count': customer_count,
                'progress_count': progress_count,
                'lunch': FoodItems.objects.filter(food_category='lunch').count(),
                'breakfast': FoodItems.objects.filter(food_category='breakfast').count(),
                'brunch': FoodItems.objects.filter(food_category='brunch').count(),
                'dinner': FoodItems.objects.filter(food_category='dinner').count(),
                'snacks': FoodItems.objects.filter(food_category='snacks').count(),
            }
            return render(request, 'admin.html', context)
        else:
            return render(request, 'index.html')
    return render(request, 'index.html')
    

def adminPanelOption(request, id):
    if id == "food-items":
        items = FoodItems.objects.all()
        return render(request, 'admin-pages/food-items.html', {'itemLists': items})
    elif id == "add-food":
        return render(request, 'admin-pages/add-food.html')
    elif id == "orders":
        orderslist=Orders.objects.filter(is_purchased=False).all()
        purchasedlist=Orders.objects.filter(is_purchased=True).all()
        return render(request, 'admin-pages/display-orders.html',{'orderslist':orderslist,'purchasedlist':purchasedlist})
    return redirect('/admin/dashboard/')

def addNewFoodItem(request):
    if request.method == 'POST':
        foodName=request.POST['food_name']
        foodRatePerQuantity=request.POST['food_rate_per_quantity']
        foodAvailableTotalQuantity=request.POST['food_available_total_quantity']
        isFoodAvailable=request.POST['is-food-available']
        foodDescription=request.POST['food_description']
        foodIngredients=request.POST['food_ingredients']
        food_pros = request.POST['food_pros']
        expiryDaysCount = request.POST['expiry_days_count']
        foodCategory = request.POST['food_category']
        getCoverImage=request.FILES['food-cover-image']
        foodStatus=False
        if isFoodAvailable=="on":
            foodStatus=True
        else:
            foodStatus=False
        try:
            formData = FoodItems(food_name=foodName, food_total_quantity=foodAvailableTotalQuantity, food_image=getCoverImage, food_rate_per_quantity=foodRatePerQuantity, food_available_total_quantity=foodAvailableTotalQuantity, food_description=foodDescription, food_ingredients=foodIngredients, food_pros=food_pros, food_category=foodCategory, currently_ordered_quantity=0, till_now_ordered_total_quantity=0, is_food_available=foodStatus, expiry_days_count=expiryDaysCount)
            formData.save()
            return render(request, 'admin-pages/add-food.html', {'status': 'success', 'occur': 'Item Added Successfully'})
        except:
            return render(request, 'admin-pages/add-food.html', {'status': 'error', 'occur': 'Something Gone Wrong'})
    return render(request, 'admin-pages/add-food.html')    

def updateFoodItem(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        foodId = data['foodId']
        foodName = data['foodName']
        foodRatePerQuantity = data['foodRatePerQuantity']
        foodAvailableTotalQuantity = data['foodAvailableTotalQuantity']

        foodDetails = FoodItems.objects.filter(food_id=foodId).first()

        foodDetails.food_total_quantity=int(foodDetails.food_total_quantity)+int(foodAvailableTotalQuantity)

        oldPrice = foodDetails.food_rate_per_quantity
        foodDetails.food_name = foodName
        foodDetails.food_rate_per_quantity = foodRatePerQuantity
        foodDetails.food_available_total_quantity = foodAvailableTotalQuantity
        foodDetails.food_old_price =oldPrice
        
        foodDetails.save()

        if foodDetails.food_available_total_quantity != 0:
            foodDetails.is_food_available=True
            foodDetails.save()

        return JsonResponse({'status': "Updated Successfully", 'status_code': 200}, status=200)
    return redirect('/admin/update-food/')
