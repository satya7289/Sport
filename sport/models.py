from django.db import models

quantity_choice = [('N','New'),('U','Used'),('D','Damaged')]

class Sport(models.Model):
    name    = models.CharField(max_length=30,unique=True)
    image   = models.ImageField(upload_to='sport/images/%Y/%m/%d/',blank=True,null=True)

    def __str__(self):
        return self.name

class Item(models.Model):
    name    =models.CharField(max_length=30)
    brand   =models.CharField(max_length=30)
    quantity=models.PositiveIntegerField()
    quality=models.CharField(max_length=10,choices=quantity_choice)
    description=models.TextField(blank=True)
    image   =models.ImageField(upload_to='item/images/%Y/%m/%d/',blank=True,null=True)
    sport_type   =models.ForeignKey(Sport,on_delete=models.CASCADE)

    def __str__(self):
        return self.name
