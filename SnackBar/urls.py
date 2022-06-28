"""SnackBar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
# from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from ModelView import views, admin
from django.views.decorators.csrf import csrf_exempt

urlpatterns = [
    path('admin/', admin.adminPanel),
    path('admin/dashboard/', admin.adminPanel),
    path('admin/<str:id>', admin.adminPanelOption),
    path('admin/add-food/', admin.addNewFoodItem),
    path('admin/update-food/', csrf_exempt(admin.updateFoodItem)),
    path('update-food-quantity/', csrf_exempt(views.updateFoodQuantity)),
    # path('admin/get-orders/', csrf_exempt(admin.fetchOrders)),
    path('admin/order-lists/<str:id>', views.displayOrderDetails),
    path('admin/find-user/', csrf_exempt(views.findUser)),
    path('admin/purchasedOrder/<str:id>', views.orderPurchased), 
    path('admin/orderPrepared/<str:id>', views.orderPrepared), 
    path('admin/orderPacked/<str:id>', views.orderPacked), 
    path('', views.index),
    path('home/', views.index),
    path('dishes/', views.dishes),
    path('addItemToCart/', views.addToCart),
    path('notifications/', csrf_exempt(views.getNotifications)),
    path('update-food-quantity/', csrf_exempt(views.updateFoodQuantity)),
    path('notification-viewing/',csrf_exempt(views.viewedNotifications)),
    path('notification-delete/',csrf_exempt(views.deleteNotifications)),
    path('book-order/', csrf_exempt(views.bookOrder)),
    path('cart/', views.displayCart),
    path('food-details/', csrf_exempt(views.foodDetails)),
    path('menu/<str:id>', views.menuDish),
    path('remove-cart/<str:id>', views.removeCartItem),
    path('order-lists/<str:id>', views.displayOrderDetails),
    path('order/', views.displayOrders),
    path('payment-success/', csrf_exempt(views.paymentSuccess)),
    path('login/', views.login),
    path('profile/', views.profile),
    path('add-tags/', csrf_exempt(views.addRecommendTags)),
    path('get-tags/', csrf_exempt(views.getTags)),
    path('profile-update/', views.updateProfile),
    path('order/invoice/<str:id>', views.GeneratePDF),
    path('signup/', views.signup),
    path('logout/', views.logout),
    path('validate-username', csrf_exempt(views.UsernameValidation)),
    path('validate-email', csrf_exempt(views.EmailValidation)),
    path('activate/<uidb64>/<token>', views.VerificationView.as_view(), name='activate'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
