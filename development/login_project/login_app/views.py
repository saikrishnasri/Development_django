from django.shortcuts import render,redirect,HttpResponseRedirect
from django.http import HttpResponse
from .models import file_data,Registrations_data,Post
from .forms import Reg_form ,post_form
from django.contrib.auth.hashers import make_password
import re



def home_view(request):
    if request.method=='POST':
        image=request.FILES['image']
        video=request.FILES['video']
        print( request.FILES['image'].name)
        user=file_data(
            image=image,
            video=video
            )
        user.save()
        return render(request,'login_app/index.html')

    else:
        return render(request,'login_app/index.html')



def reg_view(request):
    if request.method=='POST':

        username = password = ''
        firstname=request.POST['firstname']
        lastname=request.POST['lastname']
        mob=request.POST['mob']
        email=request.POST['email']
        
        username=request.POST['username']


        
        password=make_password(request.POST['password'], 'n7!(gzweq86gr3+!2k-r2=p!tl413nar5^jx)*y3k4(zl2qv')

        context=Registrations_data(
                firstname=firstname,
                lastname=lastname,
                mob=mob,
                email=email,
                username=username,
                password=password,
            )
        context.save()
    #return render(request,'login_app/login.html')
        return redirect('/..login/')
        
    else:
        return render(request,'login_app/reg.html')

    
def login_view(request):
    #print(request.session['email'])
    if request.method=='POST':
        
        email='',
        password=''
       
        if 'email' in request.POST:
            email=request.POST['email']
        if 'password' in request.POST:
            password=request.POST['password']
          
          
        if email !='' and password !='':
            user_detail=Registrations_data.objects.filter(email__iexact=email,password__exact=password)
            
            if user_detail:
                user=Registrations_data.objects.get(email=email)
                uname=user.username
                msg=uname +" already login"
                request.session['id']=user.id
                request.session['username']=user.username
                request.session['email']=user.email
                return render(request,'login_app/fetch.html',{'msg':msg})
            else:
                return HttpResponse("this is not registreds")

            
    else:
        return render(request,'login_app/login.html')
          


def logout_session_delete(request):
    try:
        del request.session['id']
        del request.session['username']
        del request.session['email']
    except KeyError:
        pass
    return render(request,'login_app/login.html') 


def post_list (request):
    posts=Post.objects.all()
    context={
           'post_list':posts
       }
    return render(request,"login_app/post_list.html",context)

def post_create(request):
    form=post_form(request.POST or None)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/')

    context={
        "form":form,
        'form_type':'Create'
            }
    return render(request,"login_app/post_create.html",context)

def Post_update(request,id):
    post=Post.objects.get(id=id)
    form=post_form(request.POST or None ,instance=post)
    if form.is_valid():
        form.save()
        return HttpResponseRedirect('/post')
    context={
            "form":form,
            'form_type':'Update'
            
    }
    return render(request,"login_app/post_create.html",context)    
    
def post_delete(request,id):
    post=Post.objects.get(id=id)
    post.delete()
    return HttpResponseRedirect('/post')