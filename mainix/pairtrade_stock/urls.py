from django.conf.urls import url
from . import views

urlpatterns = [url(r'day', views.Data_Table),
               url(r'chart',views.Trade_Profit),
                url(r'/',views.Stock_index),
               ]
