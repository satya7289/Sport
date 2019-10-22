from django.db import models

quantity_choice = [('N','New'),('U','Used'),('D','Damaged')]

class Sport(models.Model):
    name    = models.CharField(max_length=30,unique=True)
    image   = models.ImageField(upload_to='sport/images/%Y/%m/%d/',blank=True,null=True)

    def __str__(self):
        return self.name

class Item(models.Model):
    name        =models.CharField(max_length=30)
    brand       =models.CharField(max_length=30)
    quantity    =models.PositiveIntegerField()
    available   =models.PositiveIntegerField(null=True)
    quality     =models.CharField(max_length=10,choices=quantity_choice)
    description =models.TextField(blank=True)
    image       =models.ImageField(upload_to='item/images/%Y/%m/%d/',blank=True,null=True)
    sport_type  =models.ForeignKey(Sport,on_delete=models.CASCADE)

    def __str__(self):
        return self.name

class Student(models.Model):
    first_name    =models.CharField(max_length=30)
    last_name     =models.CharField(max_length=30,null=True,blank=True)
    roll_no       =models.CharField(max_length=10,unique=True)
    email         =models.EmailField()
    team          =models.ManyToManyField(Sport)

    class Meta:
        ordering = ('roll_no',)

    def __str__(self):
        return self.roll_no

class ListOfItem(models.Model):
    items           =models.ManyToManyField(Item)
    item_qunatity   =models.PositiveIntegerField()

    def __str__(self):
        return self.item_name

class Checkout(models.Model):
    student_name      =models.ManyToManyField(Student)
    item_list    =models.ForeignKey(ListOfItem,on_delete=models.CASCADE)
    date_of_issue=models.DateField(auto_now=True)

    def __str__(self):
        return self.student_name

class Checkin(models.Model):
    checkout_item =models.OneToOneField(Checkout,on_delete=models.CASCADE)
    date_of_submit=models.DateField(auto_now=True)

    def __str__(self):
        return self.checkout_item

