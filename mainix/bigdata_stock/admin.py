from django.contrib import admin
from .models import Stock_Table ,Kospi_StockName,Kosdaq_StockName,Stock_Pair_Trade

admin.site.register([Stock_Table])
admin.site.register([Kospi_StockName])
admin.site.register([Kosdaq_StockName])
admin.site.register([Stock_Pair_Trade])
