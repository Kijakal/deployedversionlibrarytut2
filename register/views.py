from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, redirect, get_object_or_404
from django.template.loader import render_to_string
from django.utils.crypto import get_random_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode

from .forms import RegisterForm, PasswordResetForm, ChangePasswordForm
from django.contrib.auth.models import User, Group

from .models import Account


# Create your views here.
def register(request):
    if request.method == "POST":
        form = RegisterForm(request.POST)
        if form.is_valid():
            uname = form.cleaned_data['username']
            form.save()
            # get the new user info and set the group for this user to LibraryMember
            user = User.objects.get(username=uname)
            lib_group = Group.objects.get(name='LibraryMember')
            user.groups.add(lib_group)
            user.save()
            return redirect('login')

        return redirect("index")
    else:
        form = RegisterForm()

    return render(request, "register.html", {"form": form})


def forgot_password(request):
    form = PasswordResetForm(request.POST or None)
    if request.method == 'POST':
        if form.is_valid():
            email = form.cleaned_data['email']
            try:
                user = get_object_or_404(User, email=email)
                token = get_random_string(length=32)
                account = Account.objects.get_or_create(user=user)
                account[0].token = token
                account[0].save()
            except Exception:
                pass
            else:
                email_context = {
                    'email': user.email,
                    'protocol': 'http',
                    'domain': request.get_host(),
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': token,
                    'user': user,
                }
                email_subject = render_to_string('password_reset_email_subject.html', email_context)
                email_body = render_to_string('password_reset_email.html', email_context)

                send_mail(
                    subject=email_subject,
                    message=email_body,
                    html_message=email_body,
                    recipient_list=[email_context['email']],
                    from_email=settings.EMAIL_HOST_USER,
                )
            return render(request, "password_reset_done.html", context={})

    context = {'form': form}
    return render(request, "password_reset_form.html", context=context)


def reset_password(request, uidb64, token):
    id = int(urlsafe_base64_decode(uidb64))
    user = get_object_or_404(User, pk=id)
    validlink = False
    form = None
    if token == user.account.token:
        validlink = True
        form = ChangePasswordForm(request.POST or None)
        if request.method == 'POST':
            account = user.account
            account.token = None
            account.save()
            if form.is_valid():
                password = form.cleaned_data['password']
                user.set_password(password)
                user.save()
                return render(request, "password_reset_complete.html", context={})
    context = {'form': form, 'validlink': validlink, }
    return render(request, "password_reset_confirm.html", context=context)
