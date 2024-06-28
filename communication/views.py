from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse

from users.models import LocalUser
from .forms import PrivateMessageForm
from .models import GlobalMessage, PrivateMessage


def global_chat(request):
    if request.method == 'POST':
        message_content = request.POST.get('content', '')
        if message_content:
            author = request.user
            message = GlobalMessage.objects.create(author=author, content=message_content)
            response_data = {
                'author': message.author.username,
                'content': message.content,
                'created_at': message.created_at.strftime("%Y-%m-%d %H:%M:%S"),
            }
            return JsonResponse(response_data)

    messages = GlobalMessage.objects.all().order_by('created_at')
    return render(request, 'communication/global_chat.html', {'messages': messages})


"""
@login_required
def write_message(request, user_id):
    recipient = get_object_or_404(LocalUser, id=user_id)
    if request.method == 'POST':
        content = request.POST.get('content', '')
        if content:
            PrivateMessage.objects.create(author=request.user, recipient=recipient, content=content)
            # Перенаправление на страницу отправки сообщения или на другую страницу
            return redirect('write_message', user_id=recipient.id)
    return render(request, 'communication/write_message.html', {'recipient': recipient})
"""


@login_required
def private_chat(request, user_id):
    recipient = get_object_or_404(LocalUser, id=user_id)
    if request.method == 'POST':
        content = request.POST.get('content', '')
        if content:
            message = PrivateMessage.objects.create(author=request.user, recipient=recipient, content=content)
            return JsonResponse({
                'author': message.author.username,
                'content': message.content,
                'created_at': message.created_at.strftime("%Y-%m-%d %H:%M")
            })

    # Основное представление для личного чата
    messages = PrivateMessage.objects.filter(
        Q(author=request.user, recipient=recipient) |
        Q(author=recipient, recipient=request.user)
    ).order_by('created_at')

    return render(request, 'communication/private_chat.html', {'messages': messages, 'recipient': recipient})

@login_required
def fetch_private_messages(request, user_id):
    recipient = get_object_or_404(LocalUser, id=user_id)
    messages = PrivateMessage.objects.filter(
        Q(author=request.user, recipient=recipient) |
        Q(author=recipient, recipient=request.user)
    ).order_by('created_at')

    messages_data = [{
        'author': message.author.username,
        'content': message.content,
        'created_at': message.created_at.strftime("%Y-%m-%d %H:%M")
    } for message in messages]

    return JsonResponse({'messages': messages_data})


