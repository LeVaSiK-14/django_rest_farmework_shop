from django.conf import settings
from django.contrib import messages
from django.core.mail import EmailMessage
from django.shortcuts import render, redirect
from django.http import HttpResponseRedirect
from .models import *
from .forms import UserRegister
from authentication.models import User
from django.contrib.auth import authenticate
from django.views import View
from django.urls import reverse
from django.utils.encoding import force_bytes, force_text, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.contrib.sites.shortcuts import get_current_site
from .utils import account_activation_token



def register(request):
    template_name = 'main_app/register.html'
    form = None
    if request.method == "POST":
        form = UserRegister(request.POST)
        email = request.POST.get('email')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Пользователь с таким email адресом уже зарегестрирован!')
        else:
            if form.is_valid():
                ins = form.save()
                username = form.cleaned_data["username"]
                password = form.cleaned_data["password1"]
                user = authenticate(username=username, password=password, email=email)
                ins.email = email
                ins.save()
                form.save_m2m()

                uidb64 = urlsafe_base64_encode(force_bytes(User.pk))
                domain=get_current_site(request).domain
                link = reverse('activate', kwargs={
                                'uidb64': uidb64, 'token':account_activation_token.make_token(user)})

                activate_url='http://'+domain+link

                email_body = 'Hi '+user.username + \
                    'Pleaseuse this link to activate your account\n' + activate_url

                email_subject = 'Activate your account!!'
                from_email = settings.EMAIL_HOST_USER
                to_list = [ins.email, settings.EMAIL_HOST_USER]

                email = EmailMessage(
                    email_subject, 
                    email_body, 
                    from_email, 
                    to_list
                )
                email.send(fail_silently=True)
                messages.success(request, 'Вы успешно зарегестрировались!')
                return redirect("/")
            
    else:
        form = UserRegister()

    context = {'form': form,}
    return render(request, template_name, context=context)

class VerificationView(View):
    def get(self, request, uidb64, token):
        return redirect('login')



def index(request):
    products = Product.objects.all()
    template_name = 'main_app/index.html'
    context = {
                'products': products,
                }
    return render(request, template_name, context=context)
