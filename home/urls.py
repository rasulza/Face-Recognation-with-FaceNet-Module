from django.urls import path
from home import views

app_name = 'home'
urlpatterns = [
    path('',views.Home_view.as_view(), name='home'),
    path('bread_status',views.BreadStatusView.as_view(),name='bread_num')
] 
