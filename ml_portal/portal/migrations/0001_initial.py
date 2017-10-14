# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings
import portal.utils


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ModelFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, blank=True)),
                ('creation_date', models.DateField(auto_now_add=True)),
                ('path', models.CharField(max_length=200, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100)),
                ('status', models.IntegerField(default=0, choices=[(0, b'expecting_training_file'), (1, b'expecting_start_training'), (2, b'training'), (3, b'expecting_test_file'), (4, b'expecting_start_evaluation'), (5, b'evaluation'), (6, b'complete')])),
                ('creation_date', models.DateField(auto_now_add=True)),
                ('modelsfile', models.ForeignKey(blank=True, to='portal.ModelFile', null=True)),
            ],
        ),
        migrations.CreateModel(
            name='TestFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, blank=True)),
                ('creation_date', models.DateField(auto_now_add=True)),
                ('path', models.CharField(max_length=200, blank=True)),
                ('docfile', models.FileField(upload_to=portal.utils.get_upload_test_path, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='TrainingFile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('title', models.CharField(max_length=100, blank=True)),
                ('creation_date', models.DateField(auto_now_add=True)),
                ('path', models.CharField(max_length=200, blank=True)),
                ('docfile', models.FileField(upload_to=portal.utils.get_upload_training_path, blank=True)),
            ],
        ),
        migrations.CreateModel(
            name='UserProfile',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('address', models.CharField(max_length=50, blank=True)),
                ('city', models.CharField(max_length=60, blank=True)),
                ('state_province', models.CharField(max_length=30, blank=True)),
                ('country', models.CharField(max_length=50, blank=True)),
                ('problem', models.OneToOneField(null=True, blank=True, to='portal.Problem')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='problem',
            name='testfile',
            field=models.ForeignKey(blank=True, to='portal.TestFile', null=True),
        ),
        migrations.AddField(
            model_name='problem',
            name='trainingfile',
            field=models.ForeignKey(blank=True, to='portal.TrainingFile', null=True),
        ),
    ]
