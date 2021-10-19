from django.db import models


# Create your models here.
class BuyerInformation(models.Model):
    buyer_name = models.CharField(max_length=200, db_index=True)
    buyer_number = models.IntegerField(db_index=True)
    buyer_location = models.CharField(max_length=200, blank=True, null=True)

    def save_buyer_info(self):
        self.save()
