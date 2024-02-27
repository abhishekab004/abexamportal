from django import forms
from django.contrib.auth.models import User
from testapp.models import Contact

class SignUpForm(forms.ModelForm):
    def clean_email(self):
        email=self.cleaned_data['email']
        if User.objects.filter(email=email).exists():
            raise ValidationError('Email already exists')
        return email
    
    username = forms.CharField(label='Username',widget=forms.TextInput(attrs={'class': 'form-control'}))
    email = forms.EmailField(label='Email',widget=forms.TextInput(attrs={'class': 'form-control'}))
    password1 = forms.CharField(label='Password',widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    password2= forms.CharField(label='Confirm Password',widget=forms.PasswordInput(attrs={'class': 'form-control'}))
    class Meta:
        model = User
        fields = ('username', 'email', 'password1','password2' )
 
 
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
       
class EmailForm(forms.Form):
    name=forms.CharField(label='Name',widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'आपका नाम '}))
    email = forms.EmailField(label='Email',widget=forms.TextInput(attrs={'class': 'form-control','placeholder': 'आपका ईमेल '}))
    send_email_to = forms.EmailField(label='Email Send To ',widget=forms.TextInput(attrs={'class': 'form-control','placeholder': ' जिनको भेजाना है उनका ईमेल'}))
    comments = forms.CharField(label='Comments',widget=forms.Textarea(attrs={'class':'form-control','placeholder': 'आपका मैसेज '}))
    
class ContactUsForm(forms.ModelForm):
    name=forms.CharField(label='Name',widget=forms.TextInput(attrs={'class':'form-control'}))
    email = forms.EmailField(label='Email',widget=forms.TextInput(attrs={'class': 'form-control'})) 
    subject=forms.CharField(label='Subject',widget=forms.TextInput(attrs={'class':'form-control'}))
    message=forms.CharField(label='Message',widget=forms.Textarea(attrs={'class':'form-control'}))
    
    
    class Meta:
        model = Contact
        fields = ('name', 'email', 'subject', 'message')
    