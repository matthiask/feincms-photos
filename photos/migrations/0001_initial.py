# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import photos.models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Album',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('title', models.CharField(max_length=100, verbose_name='title')),
                ('description', models.TextField(verbose_name='description', blank=True)),
                ('created_by', models.ForeignKey(related_name=b'+', verbose_name='created by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created'],
                'verbose_name': 'album',
                'verbose_name_plural': 'albums',
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('created', models.DateTimeField(auto_now_add=True, verbose_name='created')),
                ('modified', models.DateTimeField(auto_now=True, verbose_name='modified')),
                ('title', models.CharField(max_length=100, verbose_name='title')),
                ('photo', models.ImageField(upload_to=photos.models._upload_to, verbose_name='photo')),
                ('is_flagged', models.BooleanField(default=False, help_text='Flagged photos are only shown to administrators for deletion or un-flagging.', verbose_name='is flagged')),
                ('album', models.ForeignKey(related_name=b'photos', verbose_name='album', to='photos.Album')),
                ('created_by', models.ForeignKey(related_name=b'+', verbose_name='created by', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-created'],
                'verbose_name': 'photo',
                'verbose_name_plural': 'photos',
            },
            bases=(models.Model,),
        ),
    ]
