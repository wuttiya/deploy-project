

from tabnanny import check
from django.shortcuts import render,redirect
from django.http import HttpResponseRedirect
from django.urls import reverse
from django.http import HttpResponse
from .models import *
from songline import Sendline #อย่าลืมpip install

# def Home (request):
#     return HttpResponse('<h1>Hello World!</h1><br><br>by wuttiya uttaracha')

#image
from django.core.files.storage import FileSystemStorage
# Paginator
from django.core.paginator import Paginator

def Home (request):
    
    wcategory = Category.objects.all()
    
    allproduct = Product.objects.all()
    # pagination
    product_per_page=10
    paginator=Paginator(allproduct,product_per_page)
    page=request.GET.get('page')
    allproduct=paginator.get_page(page)
    # pagination
    print('COUNT:',len(allproduct))
    


    # context ={'allproduct':allproduct}
 
    context ={
        'allproduct':allproduct,
        'wcategory':wcategory

    }
    
    

    
    return render(request,'company/home.html',context)

def AboutUs(request):
    wcategory = Category.objects.all()
    context={'wcategory':wcategory}

    return render(request,'company/aboutus.html',context)

def ContactUs(request):
    wcategory = Category.objects.all()
    context={} #สิ่งที่จะแนบ
    if request.method == 'POST':
        data=request.POST.copy()
        title=data.get('title')
        email=data.get('email')
        detail=data.get('detail')
        print(title)
        print(email)
        print(detail)

        #กรณีที่ userไม่กรอกข้อมูล
        if title == '' and email == '' :
            context['message'] = 'กรุณากรอกข้อมูลให้ครบ'
            return render(request,'company/contact.html',context)


        #เมื่อได้ข้อมูแล้วให้ลองปริ้นดูก่อน แล้วค่อยทำการบันทึก
        #ContactList(title=title,email=email,detail=detail).save() บันทึกแบบนี้หรือแบบข้างล่างก็ได้
        newrecord = ContactList()
        newrecord.title=title
        newrecord.email=email
        newrecord.detail=detail
        newrecord.save()
        context['message']='ได้รับข้อความแล้ว'

        token='C6aUH8g6WDg2KHyCiFypUqjShyBMHjqI17Vb2Sey2WX'
        m=Sendline(token)
        m.sendtext('หัวข้อ:{}\nอีเมลล์:{}\n>>>{}'.format(title,email,detail))#.formatคือการเอาตัวแปลไปใส่ในจุด{}
    context={'wcategory':wcategory}
    return render(request,'company/contact.html',context)


from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required #บังคับให้ User ล็อกอิน ก่อนที่จะเข้าถึง


def Login(request):
    wcategory = Category.objects.all()
    context={} #สิ่งที่จะแนบ
    if request.method == 'POST':
        data=request.POST.copy()
        username=data.get('username')
        password=data.get('password')

        try:
            user=authenticate(username=username,password=password)
            login(request,user)
            return redirect('home-page')
        except:
            context['message']='username หรือ passwordไม่ถูก กรุณาองใหม่อีกครั้ง'
       
    context={'wcategory':wcategory}  

    return render(request,'company/login.html',context)


@login_required #บังคับให้ User ล็อกอิน ก่อนที่จะเข้าถึง
def Accountant (request):
    #from django.shortcuts import render,redirect
    if request.user.profile.usertype != 'accountant':  #ถ้าหากชนิดของ userไม่ใช่accountant 
        return redirect('home-page') #ส่งกลับไปหน้าhome page

    contact = ContactList.objects.all().order_by('-id')
    context= ContactList.objects.all()
    context ={'contact':contact}
    return render(request,'company/accountant.html',context)



#from django.contrib.auth.models import User
def Register(request):
    wcategory = Category.objects.all()
    context={} #สิ่งที่จะแนบ
    if request.method == 'POST':
        data=request.POST.copy()
        fullname=data.get('fullname')#.get ('fullname)คือการกรอกเข้าไปในช่องที่ชื่อname="fullname"
        mobile=data.get('mobile')
        username=data.get('username')
        password=data.get('password')
        password2=data.get('password2')
        

        
        try:
            check = User.objects.get(username=username)
            context['warning'] = 'email :  {} มีในระบบแล้ว กรุณาใช้ email อื่น'.format(username)
            return render(request,'company/register.html',context)

        except:
            if password != password2:  
                 context['warning'] = 'กรุณากรอกรหัสผ่านให้ตรงกัน'
                 return render(request,'company/register.html',context)

           
            newuser = User()
            newuser.username=username
            newuser.email = username
            newuser.first_name = fullname
            newuser.set_password(password)
            newuser.save()

            newprofile =Profile()
            newprofile.user=User.objects.get(username=username)
            newprofile.mobile=mobile
            newprofile.save()
            
        
            

        try:
            user=authenticate(username=username,password=password)          
            login(request,user)
        except:
            context['message']='username หรือ passwordไม่ถูก'
         
        return HttpResponseRedirect(reverse('success'))
       

    
       
      
    context={'wcategory':wcategory}
    return render(request,'company/register.html',context)



@login_required  #บังคับให้ User ล็อกอิน ก่อนที่จะเข้าถึง
def ProfilePage(request):
    context={} #สิ่งที่จะแนบไป if request.method =='Post':
    profileuser=Profile.objects.get(user=request.user)
    context['profile']=profileuser
    return render(request,'company/profile.html',context)


import uuid

def ResetPassword2(request):
    
    context={} #สิ่งที่จะแนบ
    if request.method == 'POST':
        data=request.POST.copy()
        username=data.get('username')
    
        try:
            user=User.objects.get(username=username)
            u=uuid.uuid1()
            token=str(u)
            newreset=ResetPassword()
            newreset.user=user
            newreset.token=token
            newreset.save()

            return redirect('home-page')
        except:
            context['message']='Email ของคุณไม่มีในระบบ กรุณาตรวจสอบใหม่'
    
    

            

            
          #  return redirect('home-page')
       # except:
       #     context['message']='username หรือ passwordไม่ถูก'
       
      

    return render(request,'company/resetpassword.html',context)





def ResetNewPassword(request,token):
    
    context={} #สิ่งที่จะแนบ
    print ('token:',token)
    try:
        check = ResetPassword.objects.get(token=token)
        if request.method == 'POST':
           data=request.POST.copy()
           password1=data.get('resetpassword1')
           password2=data.get('resetpassword2')
           if password1 == password2:
              user=check.user
              user.set_password(password1)
              user.save()
              user=authenticate(username=user.username,password=password1)          
              login(request,user)
              return redirect('profile-page')
           else:
                context['error']='รหัสผ่านทั้งสองช่อง ไม่ถูกต้อง'

 
    except:
        context['error']='ไม่สำเร็จกรุณารีเซ็ตใหม่อีกครั้ง'
    return render(request,'company/resetnewpassword.html',context)


def ActionPage(request,cid):
    #cid=ContactList ID
    context={}
    contact=ContactList.objects.get(id=cid)
    context['contact']=contact

    try:
        action=Action.objects.get(contactlist=contact)
        context['action']=action
    except:
        pass

    if request.method == 'POST':

        data=request.POST.copy()
        detail=data.get('detail')
        print(data)
        if 'save' in data:
            print('save data')
            try:
                check=Action.objects.get(contactlist=contact)
                check.actiondetail=detail
                check.save()
                context['action'] =check
            except:       
                new=Action()
                new.contactlist=contact
                new.actiondetail=detail
                new.save()

        elif 'delete' in data:
            try:
                #check=Action.objects.get(contactlist=contact)
                #check.delete()
                contact.delete()
                return redirect('accountant-page')
            except:
                pass
            
        elif 'completed' in data:
            print('mark completed')
            contact.complete=True
            contact.save()

    return render(request,'company/action.html',context)



def Addproduct(request):
    pcategory = Category.objects.all()

    if request.method == 'POST': #ถ้ามีการกดsubmit จะขอข้อมมูลจาก POST
        data=request.POST.copy() #ขอข้อมูลและcopy มาไว้ในdata
        title=data.get('title') #ยัดข้อมมูลใส่ในตัวแปลใหม่
        descripttion=data.get('descripttion')
        price=data.get('price')
        #quantity=data.get('quantity')
        stock=data.get('stock')
        instock=data.get('instock')
        cat=data.get('category')
        category = Category.objects.get(id=cat)

        print(title)
        print(descripttion)
        print(price)
        #print(quantity)
        print(instock)
        print(stock)
        print(category)


        print('File:',request.FILES)
          
        new=Product()
        new.title=title
        new.descripttion=descripttion
        new.price= float(price)
        
        #new.quantity=int(quantity)
        new.stock=int(stock)
        new.category=category
        new.save()
        if instock == 'instock':
            new.instock=True
        if 'picture' in request.FILES:

            file_image=request.FILES['picture']
            file_image_name=file_image.name.replace('','')
#from django.core.files.storage import FileSystemStorage
            fs = FileSystemStorage()
            filename=fs.save(file_image_name,file_image)
            upload_file_url =fs.url(filename)
            print('Picture URL:',upload_file_url)
            new.picture=upload_file_url[6:]#ตัดmidiaในurlเพื่อไม่ให้ซ้ำกัน
            new.save()



        if 'specfile' in request.FILES:
            file_image=request.FILES['specfile']
            file_image_name=file_image.name.replace('','')
#from django.core.files.storage import FileSystemStorage
            fs = FileSystemStorage()
            filename=fs.save(file_image_name,file_image)
            upload_file_url =fs.url(filename)
            print('Specfile URL:',upload_file_url)
            new.specfile=upload_file_url[6:]
            new.save()


    return render(request,'company/addproduct.html',{'pcategory':pcategory})


@login_required
def Buy(request,c_id):
    wcategory=Category.objects.all()
    context={}
    product=Product.objects.get(id=c_id)
    context['product'] = product
    context['wcategory']=wcategory
    
   

    return render(request,'company/buy.html',context)



def Search(request):
    context={}
    data=request.GET['title']
    print('PrintTestdata',data)
    allproduct=Product.objects.filter(title__contains=data)
    context['allproduct']=allproduct
    if not allproduct.exists():
        
        context['notsearch']='ไม่มีสินค้าที่ท่านต้องการค้นหา โปรดลองใหม่อีกครั้ง'
        
    return render(request,'company/home.html',context)



def CCategory(request):
    wcategory = Category.objects.all()
    print('longggggggggggggggggggggg')
    svalue = request.POST.get('categoryr')
    print(svalue)
    allproduct=Product.objects.filter(category__id=svalue)
    # pagination
    product_per_page=10
    paginator=Paginator(allproduct,product_per_page)
    page=request.GET.get('page')
    allproduct=paginator.get_page(page)
    # pagination
    print('12345677',allproduct)
    if not allproduct:
        allproduct=Product.objects.all()
        # pagination
        product_per_page=10
        paginator=Paginator(allproduct,product_per_page)
        page=request.GET.get('page')
        allproduct=paginator.get_page(page)
        # pagination

    contextt={
        'allproduct':allproduct,
        'wcategory':wcategory
    }

    # if not allrow.exists():
    #     allrow=Product.objects.all()
        
    return render(request,'company/home.html',contextt)



def Success(request):
    return render(request,'company/home.html')


  
from line_notify import LineNotify
def Check(request,c_id):
    context={}
    product=Product.objects.get(id=c_id)
    context['product'] = product
    if request.method == 'POST':
        data=request.POST.copy()
        firstName=data.get('firstName')
        lastName=data.get('lastName')
        address=data.get('address')
        address2=data.get('address2')
        province=data.get('province')
        zip=data.get('zip')
        quantity=data.get('quantity')
        paymentMethod=data.get('paymentMethod')
        call=data.get('call')
        picture=data.get('picture')
        if paymentMethod == 'cash_on_delivery':
            paymentMethod='เก็บเงินปลายทาง'
        else:
            paymentMethod='โอนชำระ'
        price=product.price*int(quantity)
        
        print('9999999999999999999999999')
        if 'picture' in request.FILES:
            file_image=request.FILES['picture']
            file_image_name=file_image.name.replace('','')
            print('testfile image :',file_image)
            print('testfile image_name :',file_image_name)
            fs = FileSystemStorage()
            filename=fs.save(file_image_name,file_image)
            upload_file_url =fs.url(filename)
            print('test_url :',upload_file_url)


      

        token='0Uu7AzKbcXM0j7DnKWXaxYoGe2kHD2VjCWI5MsgQrHW'
        m=Sendline(token)
        m.sendtext('สินค้า: {}\nจำนวน {} ชิ้น\nชื่อ-สกุล: {}  {}\nเบอร์มือถือ-{}\nที่อยู่: {} {} จังหวัด{} {} \nช่องทางการชำระเงิน:{}\nยอด {}'.format(product.title,quantity,firstName,lastName,call,address,address2,province,zip,paymentMethod,price))#.formatคือการเอาตัวแปลไปใส่ในจุด{}

        m.sendimage('https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcT7N8-REWZr5aETUQED3j3MDYtmDQ1g43QDS_Guf0ksgFbk69hSVyE5YAgGrMjhAw1dsD0&usqp=CAU')

        
        
        


        


        context['alert']='สั่งซื้อสำเร็จ'
    

    return render(request,'company/checkout.html',context)



# def long(request):
#     vvlue=request.POST.get('paymentMethod')
#     print('lllllllllllllllllll',vvlue)

#     return render(request,'company/checkout.html')

   


