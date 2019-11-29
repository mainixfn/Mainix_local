from django.conf.urls import url
from . import views

urlpatterns = [url(r'^', views.sig_index),
                    #url(r'^/table',views.Data_Table)
               ]