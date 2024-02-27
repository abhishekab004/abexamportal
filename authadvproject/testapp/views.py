from django.shortcuts import render,redirect
from django.contrib import messages
from django.core.mail import send_mail
from testapp.forms import EmailForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login,logout,authenticate
from testapp.forms import SignUpForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode,urlsafe_base64_encode
from django.utils.encoding import force_bytes,force_str
from testapp.tokens import account_activation_token
from django.core.mail import EmailMessage
from django.contrib.auth import get_user_model
from testapp.forms import ContactUsForm




# Create your views here.
def home_view(request):
    return render(request, 'testapp/home.html')

@login_required
def python_view(request):
    return render(request, 'testapp/python.html')

def java_view(request):
    return render(request, 'testapp/java.html')

def c_view(request):
    return render(request, 'testapp/c.html')

#signup function without email activation just only password match or not 
# def signup_view(request):
#     if request.method == 'POST':
#         form=SignUpForm(request.POST)
#         password1=request.POST.get('password1')
#         password2=request.POST.get('password2')
#         print(password1, password2)
#         if password1 != password2 :
#             messages.success(request,'Invalid Password , Make suru you have entered correct password.')
#             return redirect('/signup')
#         elif form.is_valid():
#             user=form.save()
#             user.set_password(user.password)
#             user.save()
#             messages.success(request,'The user has been signed up successfully , login to enjoy our services.')
#             return redirect('/accounts/login')
        
#     else:
#         form=SignUpForm()
#         return render(request, 'testapp/signup.html',{'form':form})
                     
#     return render(request, 'testapp/signup.html')


#signup functionality with password check and email activation link
def signup_view(request):
    form=SignUpForm()
    if request.method == 'POST':
        form=SignUpForm(request.POST)
        password1=request.POST.get('password1')
        password2=request.POST.get('password2')
        print(password1, password2)
        if password1!= password2 :
            messages.success(request,'Invalid Password, Make suru you have entered correct password.')
            return redirect('/signup')
        
        elif form.is_valid():
            user=form.save(commit=False)
            user.is_active=False
            user.set_password(user.password)
            user.save()
            
            current_site=get_current_site(request)
            mail_subject='Activate your Account'
            message= render_to_string('registration/account_activate.html',{
                'user': user,
                'domain': current_site.domain,
                'uid':urlsafe_base64_encode(force_bytes(user.pk)),
                'token':account_activation_token.make_token(user),
            })
            
            email=form.cleaned_data['email']
            email_message=EmailMessage(mail_subject,message,to=[email])
            email_message.send()
            messages.success(request,'Please check your email for the activation link')
            return redirect('/accounts/login')
    return render(request, 'testapp/signup.html',{'form':form})


# code for active account when click in email

def activate(request,uidb64,token):
    User=get_user_model()
    try:
        uid=force_str(urlsafe_base64_decode(uidb64))
        user=User.objects.get(pk=uid)
    except(TypeError,ValueError,OverflowError,User.DoesNotExist):
        user=None
    if user is not None and account_activation_token.check_token(user,token):
        user.is_active=True
        user.save()
        login(request,user)
        messages.success(request,'Your account has been activated successfully')
        return redirect('/accounts/login')
    else:
        messages.error(request,'Activation link is invalid! or expired')
        return redirect('/')
    

def logout_view(request):
    logout(request)
    messages.success(request,'your account has been logged out')
    # return render(request, 'testapp/logout.html')
    return redirect('/accounts/login')

def login_view(request):
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            messages.success(request,'your account has been logged in')
            return redirect('/python')
        else:
            messages.error(request,'invalid username or password')
    return render(request, 'testapp/loginn.html')


#email settings

def email_send(request):
    form=EmailForm()
    send=False
    if request.method == 'POST':
        form=EmailForm(request.POST)
        if form.is_valid():
            cd=form.cleaned_data
            name=cd.get('name')
            email=cd.get('email')
            comments=cd.get('comments')
            subject=f"{name}({email}) recommends you to see this Beautiful Exam preparation website for python developers"
            # web_url=request.build_absolute_uri()
            domain='http://127.0.0.1:8000/'
            message=f"Go to Website {domain} \n \n {name} send you a this. \n comments: {comments }"
            send_mail(subject,message,email,[cd['send_email_to']],fail_silently=False)
            send=True
            messages.success(request,'Mail Sent Successfully')
            return redirect('/sendemail')
    else:
        form=EmailForm()
    return render(request, 'testapp/sendemail.html', {'form': form,'send':send})

def about_us_view(request):
    return render(request, 'testapp/about_us.html')

def contact_us_view(request):
    if request.method == 'POST':
        form=ContactUsForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,'Your provided information has been sent to administrator')
            return redirect('/contactus')
    else:
        form=ContactUsForm()
        return render(request, 'testapp/contact_us.html', {'form': form})