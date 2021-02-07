from django.urls import path

from mainapp import views

urlpatterns = [
    path('', views.home, name="home"),
    path('index/', views.index, name="index"),
    path('update/', views.update, name="update"),
    path('additem/', views.additem, name="additem"),
    path('loginuser/', views.loginuser, name='loginuser'),
    path('signupuser/', views.signupuser, name='signupuser'),
    path('logout/', views.logoutuser, name = 'logoutuser'),
    path('item/<int:item_pk>', views.viewitem, name='viewitem'),
    path('item/<int:item_pk>/delete', views.deleteitem, name='deleteitem'),
]