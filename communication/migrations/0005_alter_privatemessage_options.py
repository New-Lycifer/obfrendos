# Generated by Django 5.0.4 on 2024-06-14 15:12

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('communication', '0004_chatmessage_globalmessage_privatemessage_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='privatemessage',
            options={'verbose_name': 'Личное сообщение', 'verbose_name_plural': 'Личные сообщения'},
        ),
    ]
