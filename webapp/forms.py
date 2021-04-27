from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import password_validation

from .models import CoffeeRecipe

from django import forms

from django.core.exceptions import ValidationError

class UserLoginForm(AuthenticationForm):
    def __init__(self, *args, **kwargs):
        super(UserLoginForm, self).__init__(*args, **kwargs)

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username'}))
    password = forms.CharField(widget=forms.PasswordInput(
        attrs={'class': 'form-control', 'placeholder': 'Password',}))

class RegisterForm(forms.Form):

    username = forms.CharField(widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Username'}))

    password1 = forms.CharField(
        label= "Password",
        strip=False,
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password', 'autocomplete': 'new-password'}),
        help_text=password_validation.password_validators_help_text_html()
    )
    password2 = forms.CharField(
        label= "Password Confirmation",
        widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password', 'autocomplete': 'new-password'}),
        strip=False
    )
    first_name = forms.CharField(max_length=30, required=True, help_text='Required.', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'First Name'}))
    last_name = forms.CharField(max_length=30, required=True, help_text='Required.', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.', widget=forms.TextInput(
        attrs={'class': 'form-control', 'placeholder': 'E-mail'}))

    def clean_password2(self):
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError(
                self.error_messages['password_mismatch'],
                code='password_mismatch',
            )
        return password2

    def _post_clean(self):
        super()._post_clean()
        # Validate the password after self.instance is updated with form data
        # by super().
        password = self.cleaned_data.get('password2')
        if password:
            try:
                password_validation.validate_password(password)
            except ValidationError as error:
                self.add_error('password2', error)

class CoffeeRecipeForm(forms.ModelForm):
    def __init__(self, *args, **kwargs):
        super(CoffeeRecipeForm, self).__init__(*args, **kwargs)
        self.fields['name'].widget = forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Name'})
        self.fields['image'].widget = forms.FileInput(attrs={'class': 'custom-file-input'})
        self.fields['coffee'].widget = forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'})
        self.fields['milk'].widget = forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'})
        #self.fields['water'].widget = forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'})
        self.fields['chocolate'].widget = forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'})
        self.fields['cost'].widget = forms.NumberInput(attrs={'class': 'form-control', 'placeholder': '0'})

    class Meta:
        model = CoffeeRecipe
        fields = ['name', 'image', 'coffee', 'milk', 'chocolate', 'cost']

# class RegisterForm(UserCreationForm):
#     first_name = forms.CharField(max_length=30, required=True, help_text='Required.', widget=forms.TextInput(
#         attrs={'class': 'form-control', 'placeholder': 'First Name'}))
#     last_name = forms.CharField(max_length=30, required=True, help_text='Required.', widget=forms.TextInput(
#         attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
#     email = forms.EmailField(max_length=254, help_text='Required. Inform a valid email address.', widget=forms.TextInput(
#         attrs={'class': 'form-control', 'placeholder': 'E-mail'}))

#     #overide
#     password1 = forms.CharField(
#         label= "Password",
#         strip=False,
#         widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password', 'autocomplete': 'new-password'}),
#         help_text=password_validation.password_validators_help_text_html()
#     )
#     password2 = forms.CharField(
#         label= "Password confirmation",
#         widget=forms.PasswordInput(attrs={'class': 'form-control', 'placeholder': 'Password', 'autocomplete': 'new-password'}),
#         strip=False
#     )
#     username = forms.EmailField(widget=forms.TextInput(
#         attrs={'class': 'form-control', 'placeholder': 'Username'}))
#     class Meta:
#         model = User
#         fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2', )

# class UserRegistrationForm(forms.Form):
#     username = forms.CharField(required=True, widget=forms.TextInput(
#         attrs={'class': 'form-control', 'placeholder': 'Username'}))
#     password = forms.CharField(required=True, min_length=7,widget=forms.PasswordInput(
#         attrs={'class': 'form-control', 'placeholder': 'Password',}))
#     email = forms.EmailField(required=True,label="E-mail Address", widget=forms.TextInput(
#         attrs={'class': 'form-control', 'placeholder': 'E-mail'}))
#     firstName = forms.CharField(required=True,label="First Name" ,widget=forms.TextInput(
#         attrs={'class': 'form-control', 'placeholder': 'First Name'}))
#     lastName = forms.CharField(required=True,label="Last Name", widget=forms.TextInput(
#         attrs={'class': 'form-control', 'placeholder': 'Last Name'}))
    

# class UserRegistrationForm(forms.ModelForm):
#    class Meta:
#        model = User
#        fields = '__all__'

