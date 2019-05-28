from django.urls import path
from . import views


app_name = 'users'

urlpatterns = [
    path('researchers/', views.list_researchers, name='researchers_list'),
    path('researchers/profile/<int:pk>', views.show_profile, name='profile'),
]
