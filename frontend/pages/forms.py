from django import forms
from django.core.validators import MinValueValidator, MaxValueValidator
from .models import CustomUser
import re

class CSSRegistrationForm(forms.ModelForm):
    
    first_name = forms.CharField(
        max_length=150,
        label='first name',
        error_messages={'required': 'First name is required'}
    )
    last_name = forms.CharField(
        max_length=150,
        label='last name',
        error_messages={'required': 'Last name is required'}
    )
    age = forms.IntegerField(
        min_value=18,
        max_value=100,
        label='age',
        error_messages={
            'min_value': 'Age must be at least 18',
            'max_value': 'Age must be at most 100'
        }
    )
    email = forms.EmailField(
        label='email address',
        error_messages={'invalid': 'Enter a valid email address (name@domain.com)'}
    )
    favorite_album = forms.CharField(
        required=False,
        label='favorite album'
    )
    password = forms.CharField(
        widget=forms.PasswordInput,
        label='password',
        min_length=8
    )
    password_confirm = forms.CharField(
        widget=forms.PasswordInput,
        label='confirm password'
    )
    
    class Meta:
        model = CustomUser
        fields = ['first_name', 'last_name', 'age', 'email', 'favorite_album']
    
    def clean_first_name(self):
        data = self.cleaned_data['first_name']
        if not re.match(r'^[A-Z][a-z]+$', data):
            raise forms.ValidationError('Must start with capital letter, only latin letters')
        return data
    
    def clean_last_name(self):
        data = self.cleaned_data['last_name']
        if not re.match(r'^[A-Z][a-z]+$', data):
            raise forms.ValidationError('Must start with capital letter, only latin letters')
        return data
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already registered')
        return email
    
    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        password_confirm = cleaned_data.get('password_confirm')
        
        if password and password_confirm and password != password_confirm:
            raise forms.ValidationError('Passwords do not match')
        
        return cleaned_data
    
    def save(self, commit=True):
        user = super().save(commit=False)
        user.username = self.cleaned_data['email']  # использую email как username
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class JSRegistrationForm(forms.Form):
    
    first_name = forms.CharField(max_length=150)
    last_name = forms.CharField(max_length=150)
    age = forms.IntegerField(min_value=18, max_value=100)
    email = forms.EmailField()
    favorite_album = forms.CharField(required=False)
    password = forms.CharField(min_length=8)
    
    def clean_first_name(self):
        data = self.cleaned_data['first_name']
        if not re.match(r'^[A-Z][a-z]+$', data):
            raise forms.ValidationError('First name must start with capital letter, latin only')
        return data
    
    def clean_last_name(self):
        data = self.cleaned_data['last_name']
        if not re.match(r'^[A-Z][a-z]+$', data):
            raise forms.ValidationError('Last name must start with capital letter, latin only')
        return data
    
    def clean_email(self):
        email = self.cleaned_data['email']
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('This email is already registered')
        return email
    
    def save(self):
        user = CustomUser(
            first_name=self.cleaned_data['first_name'],
            last_name=self.cleaned_data['last_name'],
            age=self.cleaned_data['age'],
            email=self.cleaned_data['email'],
            favorite_album=self.cleaned_data.get('favorite_album', ''),
            username=self.cleaned_data['email']
        )
        user.set_password(self.cleaned_data['password'])
        user.save()
        return user