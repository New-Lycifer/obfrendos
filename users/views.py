from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.shortcuts import render, redirect, get_object_or_404

from .forms import RegistrationForm, PhotoUploadForm, ProfileEditForm, ProfileForm
from .models import LocalUser


def register(request):
    title = 'Регистрация'
    if request.method == 'POST':
        # Обработка отправки формы
        user_form = RegistrationForm(request.POST)
        if user_form.is_valid():
            # Создание нового пользователя
            new_user = user_form.save(commit=False)
            # Хэширование пароля
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            # Отображение страницы успешной регистрации
            return render(request, 'registration/register_done.html', {'new_user': new_user})
    else:
        # Отображение пустой формы
        user_form = RegistrationForm()
    return render(request, 'registration/register.html', {'user_form': user_form, 'title': title})


def custom_login(request, **kwargs):
    kwargs['template_name'] = 'registration/login.html'
    kwargs['extra_context'] = {'title': 'Вход'}
    return LoginView.as_view(**kwargs)(request, **kwargs)


def profile(request, user_id):
    user = get_object_or_404(LocalUser, id=user_id)
    title = f'Профиль пользователя {user.username}'
    if request.method == 'POST':
        form = PhotoUploadForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', user_id=user.id)
    else:
        form = ProfileForm(instance=user)
    return render(request, 'users/profile.html', {'form': form, 'user': user, 'title': title})


@login_required
def edit_profile(request):
    user = request.user
    title = 'Редактировать профиль'

    if request.method == 'POST':
        form = ProfileEditForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile', user.id)
    else:
        form = ProfileEditForm(instance=user)

    return render(request, 'users/edit_profile.html', {'form': form, 'title': title, 'user': user})



def privacy_policy(request):
    return render(request, 'privacy_policy.html')

def terms_of_service(request):
    return render(request, 'terms_of_service.html')