from django.urls import path
from . import views


app_name = 'research'

urlpatterns = [
    path('', views.project_list, name='project_list'),
    path('<int:year>/<int:month>/<int:day>/<slug:project>/',
         views.project_detail, name='project_detail'),
    path('irb-record/<int:irbid>/',
         views.irb_detail, name='irb_detail'),
]