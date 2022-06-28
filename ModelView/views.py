from django.http.response import JsonResponse
from django.shortcuts import render,redirect
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
from .utils import account_activation_token
from django.urls import reverse
from django.views import View
from django.contrib import auth
from .models import Cart, UserAccounts, FoodItems, Orders, Notifications
import base64, json
from validate_email import validate_email
from django.core.files.base import ContentFile
from django.core import serializers
from PIL import Image, ImageDraw
from qrcode import *
import razorpay
import datetime
from django.utils import timezone
from django.forms.models import model_to_dict
from django.core import serializers
from django.http import HttpResponse
from django.views.generic import View
from .utils import render_to_pdf
from django.template.loader import get_template
from reportlab.pdfgen import canvas
import os
from dotenv import load_dotenv

load_dotenv()

# Create your views here.

def index(request):
    if request.user.is_authenticated:
        user = auth.get_user(request)
        if(user.username=="snackbar"):
            return redirect('/admin/')
        else:
            return render(request, 'index.html')
    return render(request, 'index.html')

def EmailValidation(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        email = data['email']
        if not validate_email(email):
            return JsonResponse({'email_error': 'Email is invalid'}, status=400)
        if UserAccounts.objects.filter(email=email).exists():
            return JsonResponse({'email_error': 'sorry email in use,choose another one '}, status=409)
        return JsonResponse({'email_valid': True})

def UsernameValidation(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data['username']
        if not str(username).isalnum():
            return JsonResponse({'username_error': 'username should only contain alphanumeric characters'}, status=400)
        if UserAccounts.objects.filter(username=username).exists():
            return JsonResponse({'username_error': 'sorry username in use,choose another one '}, status=409)
        return JsonResponse({'username_valid': True})

def signup(request):
    if request.method == "POST":
        username=request.POST['username']
        email=request.POST['email']
        mobile_no=request.POST['mobile_no']
        password=request.POST['password1']
        context = {
            'fieldValues': request.POST
        }
        if not UserAccounts.objects.filter(username=username).exists():
            if not UserAccounts.objects.filter(email=email).exists():
                if len(password) < 6:
                    messages.error(request, 'Password too short')
                    return render(request, 'signup.html', context)
                user = UserAccounts.objects.create_user(username=username, email=email, mobile_no=mobile_no)
                user.set_password(password)
                user.is_active = False
                user.save()
                current_site = get_current_site(request)
                email_body = {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                }

                link = reverse('activate', kwargs={
                               'uidb64': email_body['uid'], 'token': email_body['token']})

                email_subject = 'Activate your account'

                activate_url = 'http://'+current_site.domain+link

                email = EmailMessage(
                    email_subject,
                    'Hi '+user.username + ', Click the link below to activate your account \n'+activate_url,
                    'noreply@snackbar.com',
                    [email],
                )
                email.send(fail_silently=False)
                messages.success(request, 'Account successfully created, Check Your Mail')
                return render(request, 'signup.html')
            messages.error(request, 'Email already Registered')
            return render(request, 'signup.html', context)
        messages.error(request, 'Username is not available')
        return render(request, 'signup.html', context)
    if request.user.is_authenticated:
        return redirect('/')
    return render(request, 'signup.html')

def login(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']
        if username and password:
            user = auth.authenticate(username=username, password=password)
            if user:
                if user.is_active:
                    auth.login(request, user)
                    notification=Notifications(user_id=user.User_id,username=user.username,profile_image=user.profile_image,message="Logged In Successful")
                    notification.save()
                    if username == "snackbar":
                        return redirect('/admin/')
                    # messages.success(request, 'Welcome, ' + user.username+' you are now logged in')
                    return redirect('/dishes/')
                messages.error(request, 'Account is not active,please check your email')
                return render(request, 'login.html')
            messages.error(request, 'Invalid credentials,try again')
            return render(request, 'login.html')
        messages.error(request, 'Please fill all fields')
        return render(request, 'login.html')
    if request.user.is_authenticated:
        return redirect('/')
    return render(request, 'login.html')

class VerificationView(View):
    def get(self, request, uidb64, token):
        try:
            id = force_text(urlsafe_base64_decode(uidb64))
            user = UserAccounts.objects.get(pk=id)
            if not account_activation_token.check_token(user, token):
                return redirect('/login/'+'?message='+'User already activated')
            if user.is_active:
                return redirect('/login/')
            user.is_active = True
            user.save()

            current_site = get_current_site(request)
            
            email_subject = 'Account Activated'

            redirect_url = 'http://'+current_site.domain

            email = EmailMessage(
                email_subject,
                'Hi '+user.username + ', Your Account Activated Successfully => '+redirect_url,
                'noreply@snackbar.com',
                [user.email],
            )
            email.send(fail_silently=False)

            notification=Notifications(user_id=user.User_id,username=user.username,profile_image=user.profile_image,message="Account Activated Successfully")
            notification.save()
            messages.success(request, 'Account activated successfully')
            return redirect('/login/')
        except Exception as ex:
            pass
        return redirect('/login/')

def logout(request):
    if request.user.is_authenticated:
        username = auth.get_user(request)
        user = UserAccounts.objects.get(username=username)
        notification=Notifications(user_id=user.User_id,username=user.username,profile_image=user.profile_image,message="You're Logged Out!")
        notification.save()
        auth.logout(request)
        messages.success(request, 'You have been logged out')
        return redirect('/login/')
    else:
        return redirect('/')
    return redirect('/login/')

def dishes(request):
    items = FoodItems.objects.filter(is_food_available=True)
    # for item in items.iterator():
    #     print(item.food_image)
    # print(type(items))
    return render(request, 'dishes.html',{'itemLists': items})

def displayCart(request):
    if request.user.is_authenticated:
        username=auth.get_user(request)
        user=UserAccounts.objects.get(username=username)
        userId=user.User_id
        userCart=Cart.objects.filter(User_id=userId)
        # for item in userCart.iterator():
        #     print(item.Food_id)
        return render(request, 'cart.html',{'cartItems':userCart})
    messages.error(request, 'Login for further use')
    return render(request, 'login.html')

def foodDetails(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        Food_id = data['Food_id']
        food=FoodItems.objects.get(food_id=Food_id)
        return JsonResponse({'food_id': food.food_id, 'food_name': food.food_name, 'food_image': json.dumps(str(food.food_image)), 'food_price': food.food_rate_per_quantity, 'food_old_price':food.food_old_price,'food_available_quantity': food.food_available_total_quantity, 'available_status': food.is_food_available, 'food_category': food.food_category,'expiry_days_count':food.expiry_days_count}, status=200)
    return JsonResponse({'status': "Something Gone Wrong"}, status=404)

# @login_required(login_url='/login')
@csrf_exempt
def addToCart(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            Food_id = request.POST['Food_id']
            User_id = request.POST['User_id']
            formData = Cart(User_id=User_id,Food_id=Food_id)
            try:
                formData.save()
                # request, "dishes.html", {"addItem": True, "msgItem": "Item Added Successfully"}
                return HttpResponse('')
            except:
                return render(request, "dishes.html", {"addItem": True, "errMsgItem": "Something Gone wrong"})
        else:
            return render(request, "dishes.html", {"addItem": True})
    else:
        return HttpResponse(status=403)

def removeCartItem(request,id):
    username=auth.get_user(request)
    user=UserAccounts.objects.get(username=username)
    userId=user.User_id
    cart=Cart.objects.filter(User_id=userId, Food_id=id).first()
    if cart.delete():
        return redirect('/cart/')
    return redirect('/cart/')

def menuDish(request, id):
    items = FoodItems.objects.filter(food_category=id)
    return render(request, 'dishes.html', {'itemLists': items,'menu':id})

def displayOrders(request):
    if request.user.is_authenticated:
        username = auth.get_user(request)
        user = UserAccounts.objects.get(username=username)
        userId = user.User_id
        order=Orders.objects.filter(user_id=userId,payment_successful=True).order_by('-ordered_date')
        return render(request, 'order.html', {'orders':order})
    messages.error(request, 'Login for further use')
    return render(request, 'login.html')

def bookOrder(request):
    context = {}
    if request.method == 'POST':
        data = json.loads(request.body)
        order_list = data['order_list']
        total_price = data['total_price']
        no_of_items = data['no_of_items']
        purchasing_date = data['purchasing_date']

        username=auth.get_user(request)
        user=UserAccounts.objects.get(username=username)
        userId=user.User_id

        book_order=Orders(user_id=userId,order_list=order_list,total_price=total_price,no_of_items=no_of_items,purchasing_date=purchasing_date)
        try:
            book_order.save()
            qrcode_img = make(f'http://localhost:8000/order-lists/{book_order.order_id}')
            image_name = f'Media/qrcodes/qrcode-{book_order.order_id}'+'.png'
            qrcode_img.save(image_name)
            img = f'qrcode-{book_order.order_id}'+'.png'
            book_order.qrcode_image=img
            book_order.save()
            return JsonResponse({'status': "Order Entered Successfully", 'status_code':200, 'order_id': book_order.order_id, 'user_id':userId,'phone_no':user.mobile_no,'username':user.username,'email':user.email}, status=200)
        except:
            return JsonResponse({'status': "Something Gone Wrong"}, status=403)
    return JsonResponse({'status': "Something Gone Wrong"}, status=404)

@csrf_exempt
def paymentSuccess(request):
    if request.method == "POST":
        data = json.loads(request.body)

        order_id = data['order_id']
        amount = data['amount']

        username=auth.get_user(request)
        user=UserAccounts.objects.get(username=username)
        userId=user.User_id

        book_order = Orders.objects.filter(order_id=order_id).first()
        book_order.payment_successful=True
        book_order.save()

        orderlist = book_order.order_list
        for item in orderlist:
            get_food=FoodItems.objects.filter(food_id=item['Food_id']).first()
            beforequantity=get_food.food_available_total_quantity
            get_food.food_available_total_quantity=int(beforequantity)-int(item['Quantity'])
            total_quantity=get_food.till_now_ordered_total_quantity
            get_food.till_now_ordered_total_quantity=int(total_quantity)+int(item['Quantity'])
            get_food.save()

            if get_food.food_available_total_quantity == 0:
                get_food.is_food_available=False
                get_food.save()

        cartItems=Cart.objects.filter(User_id=userId).all()
        cartItems.delete()

        client = razorpay.Client(auth=(os.environ.get('RAZOR_KEY_ID'), os.environ.get('RAZOR_KEY_SECRET')))
        payment = client.order.create({'amount': amount, 'currency': 'INR','payment_capture': '1'})
        
        current_site = get_current_site(request)
            
        email_subject = 'Order Placed Succesfully'

        redirect_url = 'http://'+current_site.domain+'/order-lists/'+str(book_order.order_id)

        email = EmailMessage(
            email_subject,
            'Hi '+user.username + ', Payment Processed and Order Placed without any issue, \nClick the link to view your order => '+redirect_url,
            'noreply@snackbar.com',
            [user.email],
        )
        email.send(fail_silently=False)

        notification = Notifications(user_id=user.User_id, username=user.username, message="Payment Successfull and Order Placed Successfully",order_id=book_order.order_id, profile_image=user.profile_image)
        notification.save()
        return JsonResponse({'status': "Order Placed Successfully", 'status_code': 200}, status=200)
    return redirect('/home/')

def displayOrderDetails(request, id):
    order = Orders.objects.filter(order_id=id).first()
    if request.user.is_authenticated:
        username = auth.get_user(request)
        user = UserAccounts.objects.get(username=username)
        userId = user.User_id
        if order is None:
            pass
        else:
            return render(request, 'orderlist.html', {'orderdetails': order, 'username': user.username, 'orderlist': order.order_list})
    return render(request, 'index.html')

def orderPurchased(request,id):
    order=Orders.objects.filter(order_id=id).first()
    username = auth.get_user(request)
    user = UserAccounts.objects.get(username=username)
    userId = user.User_id
    if order is None:
        return redirect('/')
    else:
        order.is_purchased=True
        order.purchased_date=timezone.now()
        order.handover_date=timezone.now()
        order.save()
        current_site = get_current_site(request)

        user1 = UserAccounts.objects.get(User_id=order.user_id)

        email_subject = 'Order Purchased'

        redirect_url = 'http://'+current_site.domain+'/order'

        email = EmailMessage(
            email_subject,
            'Hi '+user1.username + ', Order Purchased Just Now, \nClick the link to view your status '+redirect_url,
            'noreply@snackbar.com',
            [user1.email],
        )
        email.send(fail_silently=False)
        notification = Notifications(user_id=user1.User_id, username=user1.username,message="Order Purchased", order_id=order.order_id, profile_image=user1.profile_image)
        notification.save()
        return render(request, 'orderlist.html', {'orderdetails': order, 'username': user.username, 'status': "Updated Successfully", 'orderlist': order.order_list})
    return redirect('/home/')

def orderPrepared(request, id):
    order=Orders.objects.filter(order_id=id).first()
    username = auth.get_user(request)
    user = UserAccounts.objects.get(username=username)
    userId = user.User_id
    if order is None:
        return redirect('/')
    else:
        order.is_prepared=True
        order.save()
        current_site = get_current_site(request)

        user1=UserAccounts.objects.get(User_id=order.user_id)

        email_subject = 'Order Prepared'

        redirect_url = 'http://'+current_site.domain+'/order-lists/'+str(order.order_id)

        email = EmailMessage(
            email_subject,
            'Hi '+user1.username +
            ', Order got Prepared, \nClick the link to view your Order '+redirect_url,
            'noreply@snackbar.com',
            [user1.email],
        )
        email.send(fail_silently=False)
        notification = Notifications(user_id=user1.User_id, username=user1.username,message="Order Prepared", order_id=order.order_id, profile_image=user1.profile_image)
        notification.save()
        return render(request, 'orderlist.html', {'orderdetails': order, 'username': user.username, 'status': "Updated Successfully", 'orderlist': order.order_list})
    return redirect('/home/')

def orderPacked(request, id):
    order = Orders.objects.filter(order_id=id).first()
    username = auth.get_user(request)
    user = UserAccounts.objects.get(username=username)
    userId = user.User_id
    if order is None:
        return redirect('/')
    else:
        order.is_packed = True
        order.save()
        current_site = get_current_site(request)

        user1=UserAccounts.objects.get(User_id=order.user_id)

        email_subject = 'Order Packed'

        redirect_url = 'http://'+current_site.domain+'/order-lists/'+str(order.order_id)

        email = EmailMessage(
            email_subject,
            'Hi '+user1.username +
            ', Your Order Packed, Get it from Now onwards. \nClick the link to view your Order => '+redirect_url,
            'noreply@snackbar.com',
            [user1.email],
        )
        email.send(fail_silently=False)
        notification = Notifications(user_id=user1.User_id, username=user1.username,message="Order Packed", order_id=order.order_id, profile_image=user1.profile_image)
        notification.save()
        return render(request, 'orderlist.html', {'orderdetails': order, 'username': user.username, 'status': "Updated Successfully", 'orderlist': order.order_list})
    return redirect('/home/')

@csrf_exempt
def findUser(request):
    if request.method == "POST":
        data = json.loads(request.body)
        order_id = data['userId']
        order = Orders.objects.filter(order_id=order_id).first()
        user = UserAccounts.objects.filter(User_id=order.user_id).first()
        return JsonResponse({'username': user.username, 'status_code': 200}, status=200)
    return redirect('/home/')

def profile(request):
    if request.user.is_authenticated:
        username = auth.get_user(request)
        user = UserAccounts.objects.get(username=username)
        return render(request, 'profile.html',{'userInfo':user})
    return redirect('/')

def updateProfile(request):
    if request.method == 'POST':
        firstname=request.POST['firstname']
        lastname=request.POST['lastname']
        address=request.POST['address']
        country=request.POST['country']
        state=request.POST['state']
        district=request.POST['district']
        pincode=request.POST['pincode']
        
        username = auth.get_user(request)
        user = UserAccounts.objects.get(username=username)

        try:
            profileImage=request.FILES['profileimage']
            user.profile_image=profileImage
            # Notifications.objects.filter(user_id=user.User_id).update(profile_image='users/'+profileImage)
        except:
            pass

        user.first_name=firstname
        user.last_name=lastname
        user.Address=address
        user.Country=country
        user.State=state
        user.District=district
        user.pincode = pincode

        user.save()
        notification = Notifications(user_id=user.User_id, username=user.username, profile_image=user.profile_image, message="Profile Updated Successfully")
        notification.save()
        messages.success(request, 'Profile Updated Successfully')
        return redirect('/profile/')
    return redirect('/profile/')

def updateProfileImage(request):
    return redirect('/profile/')

def addRecommendTags(request):
    if request.user.is_authenticated:
        username = auth.get_user(request)
        user = UserAccounts.objects.get(username=username)
        if request.method == 'POST':
            data = json.loads(request.body)
            tags = data['tags']
            user.tags=tags
            user.save()
            return JsonResponse({'addedTags': tags, 'status_code': 200}, status=200)
        return redirect('/profile/')
    return redirect('/profile/')

def getTags(request):
    if request.user.is_authenticated:
        username = auth.get_user(request)
        user = UserAccounts.objects.get(username=username)
        return JsonResponse({'existingtags': user.tags, 'status_code': 200}, status=200)
    return redirect('/profile/')

def getNotifications(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            data = json.loads(request.body)
            source = data['source']
            username = auth.get_user(request)
            user = UserAccounts.objects.get(username=username)
            notifications =Notifications.objects.filter(user_id=user.User_id).order_by('-id')[:4]
            convertJSON = serializers.serialize("json",notifications)
            convertObject = json.loads(convertJSON)
            return HttpResponse(json.dumps(convertObject), status=200)
        else:
            return JsonResponse({'notifications': {}, 'status_code': 403}, status=403)
    return redirect('/')

def viewedNotifications(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            data = json.loads(request.body)
            source = data['source']
            username = auth.get_user(request)
            user = UserAccounts.objects.get(username=username)
            notifications = Notifications.objects.filter(user_id=user.User_id).update(is_viewed=True)
            return HttpResponse("Checked Out", status=200)
        else:
            return JsonResponse({'notifications': {}, 'status_code': 403}, status=403)
    return redirect('/')

def deleteNotifications(request):
    if request.method == "POST":
        if request.user.is_authenticated:
            data = json.loads(request.body)
            source = data['source']
            username = auth.get_user(request)
            user = UserAccounts.objects.get(username=username)
            notifications = Notifications.objects.filter(user_id=user.User_id)
            for re in notifications:
                re.delete()
            return HttpResponse("Removed", status=200)
        else:
            return JsonResponse({'notifications': {}, 'status_code': 403}, status=403)
    return redirect('/')

def updateFoodQuantity(request):
    data = json.loads(request.body)
    food_id  = data['food_id']
    quantity = data['quantity']
    food_items=FoodItems.objects.filter(food_id=food_id).first()
    # food_items.till_now_ordered_total_quantity = int(food_items.till_now_ordered_total_quantity)+quantity
    # food_items.food_available_total_quantity = int(food_items.food_available_total_quantity)-quantity
    food_items.save()
    return HttpResponse({"status":"success"})

def GeneratePDF(request,id):
    template = get_template('invoice.html')   
    order = Orders.objects.filter(order_id=id).first()
    user=UserAccounts.objects.filter(User_id=order.user_id).first()
    context = {
        "orderdetails": order,
        "orderlist": order.order_list,
        "useracc":user,
    }
    # print(order.order_list)
    # html = template.render(context)
    # # return HttpResponse(html)
    # pdf = render_to_pdf('invoice.html', context)
    # # return HttpResponse(pdf, content_type='application/pdf')
    # if pdf:
    #     response = HttpResponse(pdf, content_type='application/pdf')
    #     filename = 'Snackbar_%s.pdf' %(id)
    #     # print(filename)
    #     content = "inline; filename=%s" %(filename)
    #     download = request.GET.get("download")
    #     if download:
    #         content = "attachment; filename=%s" %(filename)
    #     response['Content-Disposition'] = content
    #     return response
    return render(request,'invoice.html',context)
    # return HttpResponse("Not found")

