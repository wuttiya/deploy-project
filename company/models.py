
from django.db import models
from django.contrib.auth.models import User

class Profile(models.Model):
  user=models.OneToOneField(User,on_delete=models.CASCADE)
  usertype=models.CharField(max_length=100,default='member')
  point =models.IntegerField(default=0)
  mobile = models.CharField(max_length=200,null=True,blank=True)

  def __str__(self):
    return self.user.username



class ResetPassword(models.Model):
  user = models.ForeignKey(User,on_delete=models.CASCADE)
  token =models.CharField(max_length=100)


class Category(models.Model):
  name=models.CharField(max_length=200)

  def __str__(self):
     return self.name


class Product(models.Model):
  
  title = models.CharField(max_length=200) #บังคับให้ใส่
  descripttion=models.TextField(null=True,blank=True)#กรณีไม่ต้องใส่ค่า สามารถว่างได้ ไม่บังคับ
  
  price = models.DecimalField(max_digits=10,decimal_places=0,null=True,blank=True)#max_digits=5คือระบุตัวเลข5หลัก decimal_plass=2 ระบุทศนิยม
  quantity=models.IntegerField(default=1,null=True,blank=True)
  
  instock =models.BooleanField(default=True)#กำหนดค่าเริ่มต้นเป็นจริง
  picture=models.ImageField(upload_to='product',null=True,blank=True)
  specfile=models.FileField(upload_to='specfile',null=True,blank=True)
  updated=models.DateTimeField(auto_now=True)
  created = models.DateTimeField(auto_now_add=True)
  available=models.BooleanField(default=True)
  stock=models.IntegerField(default=1,null=True,blank=True)
  category=models.ForeignKey(Category,on_delete=models.CASCADE,default=True,null=False)
  
  def __str__(self):
      return self.title  #เมื่อเรียกmodelนี้ไปช้งาน จะเรียกชื่อtitle

      #python manage.py makemigrations
      #python manage.py migrate
        #*******ทุกครั้งที่มีการเปี่ยนข้อมูลในนี้จะต้องrun 2 คำสั่งนั้นทุกครั้ง

# class Category(models.Model):
#   name=models.ForeignKey(Product,on_delete=models.CASCADE)

#   def __str__(self):
#      return self.name



class ContactList(models.Model):
  title= models.CharField(max_length=200)
  email=models.CharField(max_length=200)
  detail=models.TextField(null=True,blank=True)
  complete=models.BooleanField(default=False)

  def __str__(self):
        return self.title


class Action(models.Model):

  contactlist = models.ForeignKey(ContactList,on_delete=models.CASCADE)
  actiondetail =models.TextField()  #ถ้าไม่ใส่null=True,blank=True คือการบังคับให้กรอก
  
  def __str__(self):
        return '{}' - '{}'.format(self.contactlist.email,self.actiondetail)








