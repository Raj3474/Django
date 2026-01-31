from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django.template.loader import render_to_string

from django.contrib.auth import login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.shortcuts import get_current_site

from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode

from orders.views import user_orders

from .forms import RegistrationForm, UserEditForm, UserAddressForm
from .token import account_activation_token
from .models import Customer, Address

# Create your views here.

@login_required
def dashboard(request):
    orders = user_orders(request)
    return render(request, 'account/dashboard/dashboard.html', {
        'section': 'profile',
        'orders': orders
    })


@login_required
def edit_details(request):
    if request.method == 'POST':
        user_form = UserEditForm(instance=request.user, data=request.POST)
        if user_form.is_valid():
            user = user_form.save(commit=False)
            user.email = user_form.cleaned_data['email']
            user.save()
    else:
        user_form = UserEditForm(instance=request.user)

    return render(request,
                  'account/dashboard/edit_details.html', {'user_form': user_form})

@login_required
def delete_user(request):
    user = Customer.objects.get(user_name=request.user)
    user.is_active = False
    user.save()
    logout(request)
    return redirect('account:delete_confirmation')


def account_register(request):

    if request.user.is_authenticated:
        return redirect('account:dashboard')

    if request.method == 'POST':
        registerForm = RegistrationForm(request.POST)
        if registerForm.is_valid():

            user = registerForm.save(commit=False)
            user.email = registerForm.cleaned_data['email']
            user.set_password(registerForm.cleaned_data['password'])
            user.is_active = False
            user.save()

            # Now, save the many-to-many data for the form.
            # >>> f.save_m2m()

            # setup email
            current_site = get_current_site(request)
            subject = 'Activate your Account'
            message = render_to_string('account/registration/account_activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': account_activation_token.make_token(user),
            })
            user.email_user(subject=subject, message=message)
            return render(request, 'account/registration/register_email_confirm.html')

    else:
        registerForm = RegistrationForm()

    return render(request, 'account/registration/register.html', {
            'form': registerForm
    })


def account_activate(request, uidb64, token):
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = Customer.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, user.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user)
        return redirect('account:dashboard')
    else:
        return render(request, 'account/registration/activation_invalid.html')


# Addresses
@login_required
def view_address(request):
    try:
        address = Address.objects.filter(customer=request.user)
    except(TypeError, ValueError, OverflowError, address.DoesNotExist):
        address = None

    # orders = Order.objects.filter(user_id=user_id).filter(billing_status=True)

    return render(request, 'account/dashboard/address.html', {
        'address' : address,
    })

@login_required
def add_address(request):

    if request.method == "POST":
        address_form = UserAddressForm(data=request.POST)
        if address_form.is_valid():
            address_form = address_form.save(commit=False)
            address_form.customer = request.user
            address_form.save()
            return HttpResponseRedirect(reverse("account:address"))
    else:
        address_form = UserAddressForm()
    return render(request, "account/dashboard/edit_address.html", {
        "form": address_form
    })

@login_required
def edit_address(request, id):
    if request.method == "POST":
        address = Address.objects.get(pk=id, customer=request.user)
        address_form = UserAddressForm(instance=address, data=request.POST)
        if address_form.is_valid():
            address_form.save()
            return HttpResponseRedirect(reverse("account:address"))
    else:
        address = Address.objects.get(pk=id, customer=request.user)
        address_form = UserAddressForm(instance=address)
    return render(request, "account/dashboard/edit_address.html", {
        "form": address_form,
        "is_edit_address": 'True'
    })

@login_required
def delete_address(request, id):
    Address.objects.filter(pk=id, customer=request.user).delete()
    Address.objects.first(customer=request.user).update(default=True)
    return redirect("account:address")

@login_required
def set_default_address(request, id):
    Address.objects.filter(customer=request.user, default=True).update(default=False)
    Address.objects.filter(pk=id, customer=request.user).update(default=True)
    return redirect("account:address")