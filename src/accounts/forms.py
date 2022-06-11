from django import forms
from django.contrib.auth import get_user_model, authenticate
from django.contrib.auth.hashers import check_password

from scraping_app.models import City, Language

User = get_user_model()


class UserLoginForm(forms.Form):
    email = forms.CharField(widget=forms.EmailInput())
    email.widget.attrs.update({'class': 'form-control'})
    password = forms.CharField(widget=forms.PasswordInput(), label='Пароль')
    password.widget.attrs.update({'class': 'form-control'})

    def clean(self, *args, **kwargs):
        email = self.cleaned_data.get('email').strip()
        password = self.cleaned_data.get('password').strip()

        if email and password:
            qs = User.objects.filter(email=email)
            if not qs.exists():
                raise forms.ValidationError('Такого пользователя нет')
            if not check_password(password, qs[0].password):
                raise forms.ValidationError('Пароль не подходит!')
            user = authenticate(email=email, password=password)
            if not user:
                raise forms.ValidationError('Этот аккаунт отключен')
        return super(UserLoginForm, self).clean(*args, **kwargs)


class UserRegistrationForm(forms.ModelForm):
    email = forms.CharField(widget=forms.EmailInput(), label='Введите email')
    email.widget.attrs.update({'class': 'form-control'})
    password = forms.CharField(widget=forms.PasswordInput(), label='Пароль')
    password.widget.attrs.update({'class': 'form-control'})
    password2 = forms.CharField(widget=forms.PasswordInput(), label='Подтверждение пароля')
    password2.widget.attrs.update({'class': 'form-control'})

    class Meta:
        model = User
        fields = {'email', }

    def clean_password2(self):
        data = self.cleaned_data
        if data['password'] != data['password2']:
            raise forms.ValidationError('Пароли не совпадают')
        return data['password2']


class UserUpdateForm(forms.Form):
    city = forms.ModelChoiceField(queryset=City.objects.all(), to_field_name='slug', required=False,
                                  widget=forms.Select(attrs={'class': "form-control"}),
                                  label='Город')
    language = forms.ModelChoiceField(queryset=Language.objects.all(), to_field_name='slug', required=False,
                                      widget=forms.Select(attrs={'class': "form-control mb-3"}),
                                      label='Язык программирования')
    send_email = forms.BooleanField(required=False, widget=forms.CheckboxInput, label='Получать рассылку?')
    send_email.widget.attrs.update({'class': 'form-check-input', 'id': 'flexCheckChecked'})

    class Meta:
        model = User
        fields = {'city', 'language', 'send_email'}


class ContactForm(forms.Form):
    input_area = forms.CharField(required=True,
                                 widget=forms.TextInput(attrs={'class': "form-control"}),
                                 label='Введите сообщение')
    email = forms.EmailField(required=True,
                             widget=forms.EmailInput(attrs={'class': "form-control"}),
                             label='Введите email')
