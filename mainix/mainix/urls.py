from django.contrib import admin
from django.conf.urls import url,include

urlpatterns = [url('admin/', admin.site.urls),
               url('',include('home.urls')),
               url('signal/pairtrade/stock',include('pairtrade_stock.urls')),
               url('signal/bigdata/crypto',include('bigdata_crypto.urls'))
               ]