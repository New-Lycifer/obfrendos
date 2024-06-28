from django import forms
from django.contrib.auth.models import User
from django.forms import ClearableFileInput

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
            'bdate': 'Дата рождения'
        }
        help_texts = {
            'bdate': 'Введите дату рождения...'
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


class CustomClearableFileInput(ClearableFileInput):
    initial_text = ('')
    clear_checkbox_label = ('удалить фото')
    input_text = ('Изменить')

    def __init__(self, attrs=None):
        if attrs is None:
            attrs = {}
        # Добавляем стиль для отступа между строками
        attrs['style'] = 'margin-top: 15px;'  # Пример отступа в 10 пикселей
        attrs['class'] = 'custom-clearable-file-input'  # Пример класса для общего стиля
        super().__init__(attrs)

    def render(self, name, value, attrs=None, renderer=None):
        # Рендерим виджет и добавляем кастомные CSS классы
        rendered = super().render(name, value, attrs, renderer)
        return rendered

    def format_value(self, value):
        # Форматируем значение, если необходимо
        return super().format_value(value)

class ProfileEditForm(forms.ModelForm):
    class Meta:
        model = LocalUser
        fields = ['username', 'first_name', 'last_name', 'bdate', 'email', 'photo']
        labels = {
            'username': 'Имя пользователя',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'bdate': 'Дата рождения',
            'email': 'Email',
            'photo': 'Фото профиля',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'first_name': forms.TextInput(attrs={'class': 'form-control'}),
            'last_name': forms.TextInput(attrs={'class': 'form-control'}),
            'bdate': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            'photo': CustomClearableFileInput,
        }


class PrivateMessageForm(forms.Form):
    recipient = forms.ModelChoiceField(queryset=LocalUser.objects.all(), label='Получатель')
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 50}), label='Сообщение')