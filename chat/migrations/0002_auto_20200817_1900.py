# Generated by Django 3.1 on 2020-08-17 19:00

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('chat', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='requests',
            name='receiver',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='requests_receiver', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='requests',
            name='sender',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='requests_sender', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='message',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='message',
            name='chatroom',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='chat.chatroom'),
        ),
        migrations.AddField(
            model_name='chatroompermission',
            name='chatroom',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='chat.chatroom'),
        ),
        migrations.AddField(
            model_name='chatroompermission',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
        ),
    ]