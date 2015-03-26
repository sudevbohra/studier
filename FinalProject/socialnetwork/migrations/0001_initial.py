# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
from django.conf import settings


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Classroom',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('question', models.CharField(max_length=150, blank=True)),
                ('answer', models.CharField(max_length=150, blank=True)),
                ('upvotes', models.IntegerField(blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Documents',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('documents_url', models.CharField(max_length=150, blank=True)),
                ('upvotes', models.IntegerField(blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Student',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('school', models.CharField(max_length=430, blank=True)),
                ('major', models.CharField(max_length=430, blank=True)),
                ('interests', models.CharField(max_length=430, blank=True)),
                ('linkedin', models.CharField(max_length=430, blank=True)),
                ('picture_url', models.CharField(max_length=256, blank=True)),
                ('answer_rating', models.IntegerField(blank=True)),
                ('collab_rating', models.IntegerField(blank=True)),
                ('endorsements', models.CharField(max_length=430, blank=True)),
                ('friends', models.ManyToManyField(related_name='friends_rel_+', to='socialnetwork.Student')),
                ('user', models.OneToOneField(to=settings.AUTH_USER_MODEL)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='StudyGroup',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('start_time', models.DateTimeField()),
                ('end_time', models.DateTimeField()),
                ('active', models.BooleanField()),
                ('course', models.CharField(max_length=10)),
                ('topic', models.CharField(max_length=100)),
                ('description', models.CharField(max_length=255)),
                ('location_room', models.CharField(max_length=50)),
                ('location_name', models.CharField(max_length=255)),
                ('location_latitude', models.FloatField()),
                ('location_longitude', models.FloatField()),
                ('members', models.ManyToManyField(related_name='member', to='socialnetwork.Student')),
                ('owner', models.OneToOneField(to='socialnetwork.Student')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='documents',
            name='owner',
            field=models.OneToOneField(to='socialnetwork.Student'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='classroom',
            name='comments',
            field=models.ManyToManyField(to='socialnetwork.Comment'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='classroom',
            name='documents',
            field=models.ManyToManyField(to='socialnetwork.Documents'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='classroom',
            name='students',
            field=models.ManyToManyField(to='socialnetwork.Student'),
            preserve_default=True,
        ),
    ]
