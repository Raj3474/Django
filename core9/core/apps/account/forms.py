from django import forms
from django.contrib.auth.forms import (AuthenticationForm, PasswordResetForm, SetPasswordForm)
from .models import Customer, Address

class RegistrationForm(forms.ModelForm):
    user_name = forms.CharField(
        label='Enter Username', min_length=4, max_length=50, help_text='Required')
    email = forms.EmailField(
        max_length=100, help_text='Required', error_messages={'required': 'Sorry, you will need an email'})
    password = forms.CharField(label='Password', widget=forms.PasswordInput,)
    password2 = forms.CharField(label='Confirm password', widget=forms.PasswordInput)

    class Meta:
        model = Customer
        fields = ('user_name', 'email',)

    def clean_username(self):
        user_name = self.cleaned_data['user_name'].lower()
        r = Customer.objects.filter(user_name=user_name)
        if r.count():
            raise forms.ValidationError("Username already exists")
        return user_name

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Passwords do not match')
        return cd['password2']

    def clean_email(self):
        email = self.cleaned_data['email']
        if Customer.objects.filter(email=email).exists():
            raise forms.ValidationError("Please use another Email, that is already taken")
        return email


    # updating form fields attributes

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.fields['user_name'].widget.attrs.update(
            {
                'class': 'form-control mb-3',
                'placeholder': 'Username'
            })

        self.fields['email'].widget.attrs.update(
            {
                'class': 'form-control mb-3',
                'placeholder': 'E-mail',
                'name': 'email',
            })

        self.fields['password'].widget.attrs.update(
            {
                'class': 'form-control mb-3',
                'placeholder': 'password'
            })

        self.fields['password2'].widget.attrs.update(
            {
                'class': 'form-control mb-3',
                'placeholder': 'confirm password'
            })

# it is an extended of Django AuthenticationForm
class UserLoginForm(AuthenticationForm):

    username = forms.CharField(widget=forms.TextInput(
        attrs={
            'class': 'form-control mb-3',
            'placeholder': 'Username',
            'id': 'login-username',
        }
    ))

    password = forms.CharField(widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'Password',
            'id': 'login-pwd',
        }
    ))


class UserEditForm(forms.ModelForm):

    email = forms.EmailField(
        label='Account email (can not be changed)', max_length=200, widget=forms.TextInput(
            attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Email',
                'id': 'form-email',
                'readonly': 'readonly'
            }
    ))

    user_name = forms.CharField(
        label='Username', max_length=50, widget=forms.TextInput(
            attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Username',
                'id': 'form-username',
            }
    ))

    first_name = forms.CharField(
        label='Firstname', max_length=50, widget=forms.TextInput(
            attrs={
                'class': 'form-control mb-3',
                'placeholder': 'Firstname',
                'id': 'form-firstname',
            }
    ))

    def clean_email(self):
        email = self.cleaned_data['email']
        if not Customer.objects.filter(email=email).exists():
            raise forms.ValidationError("You are not allowed to update your email")
        return email

    class Meta:
        model = Customer
        fields = ('email', 'user_name', 'first_name',)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['user_name'].required = True
        self.fields['email'].required = True
        self.fields['first_name'].required = False


class PwdResetForm(PasswordResetForm):
    email = forms.EmailField(max_length=24, widget=forms.TextInput(
        attrs={'class': 'form-control mb-3',
               'placeholder': 'Email',
               'id': 'form-email'
        }
        ))
    def clean_email(self):
        email = self.cleaned_data['email']
        u = Customer.objects.filter(email=email)

        if not u or u.first().is_active == False:
            raise forms.ValidationError(
                'Unfortunatley we can not find that email address')
        return email


class PwdResetConfirmForm(SetPasswordForm):

    new_password1 = forms.CharField(
        label='New Password', widget=forms.PasswordInput(
            attrs={
                'class': 'form-control mb-3', 'placeholder': 'New Password',
                'id': 'form-newpass'
            })
        )

    new_password2 = forms.CharField(
        label='New Password', widget=forms.PasswordInput(
            attrs={
                'class': 'form-control mb-3', 'placeholder': 'Confirm New Password',
                'id': 'form-newpass2'
            })
        )

    # form validation for this will be done by the django default view


class UserAddressForm(forms.ModelForm):


    class Meta:
        model = Address
        fields = ["full_name", "phone", "address_line1", "address_line2", "town_city", "postcode"]

    def __init__(self, *args, **kwargs):

        super().__init__(*args,**kwargs)

        self.fields["full_name"].widget.attrs.update(
            {'class': "form-control mb-2 account-form", "placeholder": "Full Name"}
        )

        self.fields["phone"].widget.attrs.update(
            {'class': "form-control mb-2 account-form", "placeholder": "phone"}
        )

        self.fields["address_line1"].widget.attrs.update(
            {'class': "form-control mb-2 account-form", "placeholder": "Address Line 2"}
        )

        self.fields["address_line2"].widget.attrs.update(
            {'class': "form-control mb-2 account-form", "placeholder": "Address Line 2"}
        )

        self.fields["town_city"].widget.attrs.update(
            {'class': "form-control mb-2 account-form", "placeholder": "Town City"}
        )

        self.fields["postcode"].widget.attrs.update(
            {'class': "form-control mb-2 account-form", "placeholder": "PostCode"}
        )