# Import necessary libraries
from django.db import models

class TopVolume(models.Model):

    Symbol = models.CharField(max_length=255, primary_key=True)

    Company = models.CharField(max_length=255)

    Price = models.FloatField()

    Percentage_Net_Change = models.FloatField()

    Volume = models.FloatField()

    Average_Volume = models.IntegerField()

    Date = models.DateField()


    class Meta:
        db_table = 'top_volume_table'
        managed = False