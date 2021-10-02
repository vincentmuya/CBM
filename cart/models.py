from django.db import models


# Create your models here.
class BuyerInformation(models.Model):

    buyer_name = models.CharField(max_length=200, db_index=True)
    buyer_number = models.CharField(max_length=200, db_index=True)
    buyer_location = models.IntegerField(blank = True, null = True )
