
from django.urls import path
from . import views

app_name = 'tourism'
urlpatterns = [
    path('', views.index, name='index'),
    path('district/<slug:slug>/', views.district_view, name='district'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('admin/login/', views.admin_login_view, name='admin_login'),
    path('logout/', views.logout_view, name='logout'),
    path('user_dashboard/', views.user_dashboard, name='user_dashboard'),
    path('admin_dashboard/', views.admin_dashboard, name='admin_dashboard'),
    path('sos/', views.sos_alert, name='sos_alert'),

]