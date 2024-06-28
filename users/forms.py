from django import forms
from django.contrib.auth.models import User

from users.models import LocalUser


class RegistrationForm(forms.ModelForm):
    # Поля пароля и подтверждения пароля
    password = forms.CharField(label='Пароль', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Повторите пароль', widget=forms.PasswordInput)

    class Meta:
        # Модель, используемая для создания формы
        model = LocalUser
        # Поля, которые должны быть включены в форму
        fields = ('username', 'first_name', 'last_name', 'bdate', 'email')
        widgets = {
            'bdate': forms.DateInput(attrs={'type': 'date'})
        }
        labels = {
            'bdate': 'Date of Birth'
        }
        help_texts = {
            'bdate': 'Enter your date of birth'
        }

    def clean_password2(self):
        # Проверка совпадения паролей
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise forms.ValidationError('Пароли не совпадают.')
        return cd['password2']


class ProfileForm(forms.ModelForm):
    class Meta:
        model = LocalUser  # Указываем модель, с которой работает форма
        fields = ['photo', 'username', 'first_name', 'last_name', 'bdate', 'email', 'registerdate']
        photo = forms.ImageField(label='Photo', required=False)  # Добавляем поле для загрузки фотографии

class PhotoUploadForm(forms.ModelForm):
    class LocalMeta:
        model = LocalUser
        fields = ['photo']


class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = LocalUser
        fields = ['photo', 'first_name', 'last_name', 'bdate', 'email']
        widgets = {
            'bdate': forms.DateInput(attrs={'type': 'date'})
        }
        labels = {
            'username': 'Имя пользователя',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'Email',
            'bdate': 'Дата рождения',
            'photo': 'Фото'
        }
        help_texts = {
            'bdate': 'Введите дату рождения....'
        }


class PrivateMessageForm(forms.Form):
    recipient = forms.ModelChoiceField(queryset=LocalUser.objects.all(), label='Получатель')
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 50}), label='Сообщение')