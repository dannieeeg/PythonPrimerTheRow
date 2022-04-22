from django.urls import path

from . import views

urlpatterns = [
	#Leave as empty string for base url
	path('', views.store, name="store"),
	path('home/', views.cart, name="home"),
	path('cart/', views.cart, name="cart"),
	path('checkout/', views.checkout, name="checkout"),
    path('members/', views.members, name = "members"),
    path('exclusive/', views.exclusive, name = "exclusive"),
	path('members/loginPage/', views.loginPage, name = "loginPage"),
    path('logout/', views.logoutUser, name = "logout"),
    path('members/register/', views.register, name = "register"),

path('update_item/', views.updateItem, name="update_item"),
path('process_order/', views.processOrder, name="process_order"),

]