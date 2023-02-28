from django.urls import path
from .views import *

urlpatterns = [
    path('', Home,name='home-page'),#localhost8000
    path('about/', AboutUs,name='about-page'),#localhost:8000/about
    path('contact/', ContactUs,name='contact-page'),
    path('accountant/', Accountant,name='accountant-page'),
    path('register/', Register,name='register-page'),
    path('profile/', ProfilePage,name='profile-page'),
    path('resetpassword/', ResetPassword2,name='resetpassword-page'),
    path('resetnewpassword/<str:token>/', ResetNewPassword,name='resetnewpassword-page'),
    path('action-detail/<int:cid>/', ActionPage,name='action-page'),
    path('buy/<int:c_id>/', Buy,name='buy-page'),
    path('addproduct/', Addproduct,name='addproduct-page'),
    path('search/', Search,name='search-page'),
    path('categoryy/', CCategory,name='category-page'),
    path('sucess/', CCategory,name='success'),
    path('checkout/<int:c_id>/', Check,name='checkout-page'),
    
]
