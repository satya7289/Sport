from django.db import models

quantity_choice = [('New','New'),('Used','Used'),('Damaged','Damaged'),('Lost','Lost')]

class Sport(models.Model):
    name        =models.CharField(max_length=30,unique=True)
    image       =models.ImageField(upload_to='sport/images/%Y/%m/%d/',blank=True,null=True)
    created_at  =models.DateField(blank=True, null=True)
    updated_at  =models.DateField(auto_now=True)

    class Meta:
        ordering =('name',)

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
    created_at  =models.DateField(blank=True, null=True)
    updated_at  =models.DateField(auto_now=True) 

    class Meta:
        ordering =('-updated_at','id')

    def __str__(self):
        return self.name

class Student(models.Model):
    first_name    =models.CharField(max_length=30)
    last_name     =models.CharField(max_length=30,null=True,blank=True)
    roll_no       =models.CharField(max_length=10,unique=True)
    email         =models.EmailField()
    team          =models.ManyToManyField(Sport)
    created_at  =models.DateField(blank=True, null=True)
    updated_at    =models.DateField(auto_now=True)

    class Meta:
        ordering = ('-updated_at','roll_no')

    def __str__(self):
        return self.roll_no

class ListOfItem(models.Model):
    item           =models.ForeignKey(Item,on_delete=models.CASCADE)
    item_quantity   =models.PositiveIntegerField()
    date            =models.DateField(auto_now=True)

    def __str__(self):
        return '%s %s %s %s' %(self.item.sport_type.name,self.item.name,"/-",self.date)

class Checkout(models.Model):
    student_name =models.ForeignKey(Student,on_delete=models.CASCADE)
    item_list    =models.ManyToManyField(ListOfItem,blank=True)
    date_of_issue=models.DateField(auto_now=True)
    checkin_status=models.BooleanField(default=False)

    class Meta:
        ordering =('-date_of_issue','checkin_status')

    def __str__(self):
        return '%s %s' % (self.date_of_issue, self.student_name.first_name)

class Checkin(models.Model):
    checkout_item =models.OneToOneField(Checkout,on_delete=models.CASCADE)
    date_of_submit=models.DateField(auto_now=True)
    created_at  =models.DateField(blank=True, null=True)
    updated_at  =models.DateField(auto_now=True)
    remarks     =models.TextField(blank=True,null=True)    
    

    def __str__(self):
        return '%s %s %s' %(self.date_of_submit,"/-",self.checkout_item)

