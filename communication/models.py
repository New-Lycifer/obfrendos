from django.db import models

from users.models import LocalUser


class Message(models.Model):
    author = models.ForeignKey(LocalUser, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = False

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.author.username}: {self.content[:20]}'


class GlobalMessage(Message):
    pass


class ChatMessage(Message):
    chat_id = models.IntegerField()


class PrivateMessage(Message):
    recipient = models.ForeignKey(LocalUser, on_delete=models.CASCADE, related_name='received_messages')

    class Meta:
        verbose_name = 'Личное сообщение'
        verbose_name_plural = 'Личные сообщения'

    def __str__(self):
        return f'From {self.author.username} to {self.recipient.username}: {self.content[:20]}'
