from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.signup_view, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    path('add/', views.add_weight, name='add_weight'),
    path('list/', views.list_weights, name='list_weights'),

    path('edit/<int:id>/', views.edit_weight, name='edit_weight'),
    path('delete/<int:id>/', views.delete_weight, name='delete_weight'),

    path('loss/', views.weight_loss_between_dates, name='WeightLossBetweenDates'),
    path('', views.home, name='home'),
]
