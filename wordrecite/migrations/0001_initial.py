# -*- coding: utf-8 -*-
# Generated by Django 1.11.8 on 2018-06-29 06:40
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Note',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', models.TextField()),
                ('shared', models.BooleanField(default=True)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
            ],
        ),
        migrations.CreateModel(
            name='Task',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('date', models.DateField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserMore',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('daily_words', models.IntegerField(default=50)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='UserWord',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('learntimes', models.IntegerField(default=0)),
                ('date', models.DateTimeField(default=django.utils.timezone.now)),
                ('task', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='taskwords', to='wordrecite.Task')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='words', to='wordrecite.UserMore')),
            ],
        ),
        migrations.CreateModel(
            name='Vocabulary',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
        migrations.CreateModel(
            name='Word',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('explanation', models.TextField(default='')),
                ('example', models.TextField(default='')),
                ('vocabularys', models.ManyToManyField(related_name='words', to='wordrecite.Vocabulary')),
            ],
        ),
        migrations.AddField(
            model_name='userword',
            name='vocabulary',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='vocabularywords', to='wordrecite.Vocabulary'),
        ),
        migrations.AddField(
            model_name='userword',
            name='word',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wordrecite.Word'),
        ),
        migrations.AddField(
            model_name='usermore',
            name='vocabulary',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='wordrecite.Vocabulary'),
        ),
        migrations.AddField(
            model_name='task',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='task', to='wordrecite.UserMore'),
        ),
        migrations.AddField(
            model_name='note',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='notes', to='wordrecite.UserMore'),
        ),
        migrations.AddField(
            model_name='note',
            name='word',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='wordnotes', to='wordrecite.Word'),
        ),
    ]
