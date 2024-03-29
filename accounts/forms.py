from django.contrib.auth.forms import AuthenticationForm
from django import forms


class LoginForm(AuthenticationForm):
    username = forms.CharField(label="Username", max_length=30,
                               widget=forms.TextInput(attrs={'class': 'inpuser', 'name': 'username'}))
    password = forms.CharField(label="Password", max_length=30,
                               widget=forms.PasswordInput(attrs={'class': 'inppassword', 'name': 'password'}))
    

class CreateUserForm(forms.Form):
    username = forms.CharField(label='Username', max_length=20,widget=forms.TextInput(attrs={
                                   'class': 'inpuser', 'name': 'username'
                                })
                                )
    email = forms.EmailField(label='Email Id', max_length=30, widget=forms.EmailInput(attrs={
                                    'class': 'inpemail', 'name': 'email'
                                })
                                )
    number = forms.CharField(label='Mobile Number',max_length=13,widget=forms.TextInput(attrs={
                                   'class': 'inpnumber', 'name': 'number'
                               }))
    firstname = forms.CharField(label='First Name', max_length=20,widget=forms.TextInput(attrs={
                                   'class': 'inpfname', 'name': 'firstname'
                                })
                                )
    lastname = forms.CharField(label='Last Name', max_length=20,widget=forms.TextInput(attrs={
                                   'class': 'inplname', 'name': 'lastname'
                                })
                                )
    password = forms.CharField(label='Password',max_length=20,widget=forms.PasswordInput(attrs={
                                    'class': 'inppassword', 'name':'password'
                                })
                                )
    confirmpassword = forms.CharField(label='Confirm Password',max_length=20,widget=forms.PasswordInput(attrs={
                                    'class': 'inppassword', 'name':'confirmpassword'
                                })
                                )