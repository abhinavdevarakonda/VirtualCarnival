from django import forms

''' A ModelForm for creating a new user.
    It has three fields: username (from the user model), password1, and password2. 
    It verifies that password1 and password2 match, validates the password using validate_password(), 
    and sets the user’s password using set_password().
'''
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from account.models import Account


class RegistrationForm(UserCreationForm):

    #since UserCreationForm has only username, password and confirm password, I will add an email field as well using forms.EmailField()
    email = forms.EmailField(max_length=255,help_text="this field is required/enter a valid email address.")


    class Meta:
        model   = Account
        fields  = ('email','username','password1','password2')

    
    '''django will run the function after submission if the function has clean_ preceding the field name'''
    #some magic

    def clean_email(self):
        email   = self.cleaned_data['email'].lower() #email always lower
        try:
            account = Account.object.get(email=email) #Account.object will look through all fields, and get will return a single row (.filter for many rows)
        except Exception as e:
            return email
        raise forms.ValidationError(f"email {email} is already in use.")
    

    def clean_username(self):
        username   = self.cleaned_data['username']
        try:
            account = Account.object.get(username=username) 
        except Exception as e:
            return username
        raise forms.ValidationError(f"username {username} is already in use.")


class AccountAuthenticationForm(forms.ModelForm):
    
    password = forms.CharField(label="password",widget=forms.PasswordInput) #widget that hides text when typing password


    class Meta:
        model   = Account
        fields  = ("email","password")


    def clean(self):
        if self.is_valid():
            email = self.cleaned_data["email"]
            password = self.cleaned_data["password"]
            
            if not authenticate(email=email,password=password):
                raise forms.ValidationError("Invalid Username/Password")













