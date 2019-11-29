from django.db import models

class Tredn_Sig_Table(models.Model) :
    Date = models.CharField(max_length=20)
    CoinName = models.CharField(max_length=50)
    Price = models.CharField(max_length=30)
    Signal = models.CharField(max_length=30)
    Profit = models.CharField(max_length=30)

    def __str__(self):
        return self.Date



# Create your models here.
