# forms.py
from django import forms

from users.models import LocalUser
from .models import Message


class MessageForm(forms.ModelForm):
    class Meta:
        model = Message
        fields = ['content']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 2, 'placeholder': 'Enter your message...'}),
        }


class PrivateMessageForm(forms.Form):
    recipient = forms.ModelChoiceField(queryset=LocalUser.objects.all(), label='Получатель')
    content = forms.CharField(widget=forms.Textarea(attrs={'rows': 4, 'cols': 50}), label='Сообщение')