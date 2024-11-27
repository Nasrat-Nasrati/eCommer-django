from django.shortcuts import render,redirect

from .forms import RagistrationForm
from .models import Account
from django.contrib import messages,auth
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

# varification email 
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.utils.encoding import force_bytes
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import EmailMessage




def register(request):
    if request.method =="POST":
        form = RagistrationForm(request.POST)
        if form.is_valid():
            first_name = form.cleaned_data['first_name']
            last_name = form.cleaned_data['last_name']
            email = form.cleaned_data['email']
            phone_number = form.cleaned_data['phone_number']
            password = form.cleaned_data['password']

            username = email.split("@")[0] 
            user = Account.objects.create_user(first_name=first_name,last_name = last_name,email = email,username=username,password= password)
            user.phone_number = phone_number
            user.save()



            # Activation user by email address
            current_site = get_current_site(request)
            mail_subject = 'Please activate your account!'
            message = render_to_string('accounts/account_verification_email.html', {
                'user': user,
                'domain': current_site,  # Add `.domain` to get the actual domain
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),  # Correct encoding
                'token': default_token_generator.make_token(user),  # Generate the activation token
            })
            to_email = user.email  # Ensure `user.email` is used to fetch the email address
            send_email = EmailMessage(mail_subject, message, to=[to_email])
            send_email.send()
            #messages.success(request,'Thank you for ragistering with us.We have send you and email varification to your email address . Please verify it.')
            return redirect('/accounts/login?command=verification&email='+email)
    else:
        form = RagistrationForm()
    context = {
        'form':form,
    }
    return render(request,'accounts/register.html',context)



def login(request):
    if request.method =='POST':

        email = request.POST['email']
        password = request.POST['password']
        user = auth.authenticate(request, email=email, password=password) 
        if user is not None:
            auth.login(request, user)
            messages.success(request,'Your now login')
            return redirect('dashboard') 
        else:
            messages.error(request,'Invalid login credintial')
            return redirect('login')

    return render(request,'accounts/login.html')

@login_required(login_url = 'login')
def logout(request):
    auth.logout(request)
    messages.success(request,'Your logged out.')
    return redirect('login')



def activate(request,uidb64,token):
    try:
        uid=urlsafe_base64_decode(uidb64).decode()
        user = Account._default_manager.get(pk=uid)
    except(TypeError,ValueError,OverflowError,Account.DoesNotExist):
        user=None

    if user is not None and default_token_generator.check_token(user,token):
        user.is_active = True
        user.save()
        messages.success(request,'Congritulation your account is actived')
        return redirect('login')
    else:
        messages.error(request,'Invalid activation link')
        return redirect('register')
    

#this is the dashboard section 
@login_required(login_url = 'login')
def dashboard(request):
    return render(request,'accounts/dashboard.html')


    

