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
                ('name', models.CharField(max_length=40, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Comment',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=160, null=True)),
                ('date', models.DateTimeField(auto_now_add=True, null=True)),
                ('upvotes', models.IntegerField(default=0, blank=True)),
                ('attachment_url', models.CharField(max_length=256, blank=True)),
                ('attachment_name', models.CharField(max_length=200, blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Documents',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=40, blank=True)),
                ('documents_url', models.CharField(max_length=150, blank=True)),
                ('upvotes', models.IntegerField(blank=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Notification',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=80, blank=True)),
                ('picture_url', models.CharField(default=b'...', max_length=256, blank=True)),
                ('link', models.CharField(max_length=150, blank=True)),
                ('yes_link', models.CharField(max_length=150, null=True, blank=True)),
                ('no_link', models.CharField(max_length=150, null=True, blank=True)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('persistent', models.BooleanField(default=False)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('group_name', models.CharField(max_length=40, blank=True)),
                ('location', models.CharField(max_length=40, blank=True)),
                ('text', models.CharField(max_length=4000)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('upvotes', models.IntegerField(default=0, blank=True)),
                ('title', models.CharField(max_length=200)),
                ('attachment_url', models.CharField(max_length=256, blank=True)),
                ('attachment_name', models.CharField(max_length=200, blank=True)),
                ('classroom', models.ForeignKey(related_name='posts', to='socialnetwork.Classroom', null=True)),
                ('comments', models.ManyToManyField(to='socialnetwork.Comment')),
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
                ('answer_rating', models.IntegerField(null=True, blank=True)),
                ('collab_rating', models.IntegerField(null=True, blank=True)),
                ('endorsements', models.CharField(max_length=430, blank=True)),
                ('age', models.IntegerField(blank=True)),
                ('picture_url', models.CharField(default=b'https://s3-us-west-2.amazonaws.com/final-project-webapps/gates.jpg', max_length=256, blank=True)),
                ('friends', models.ManyToManyField(related_name='friends_rel_+', to='socialnetwork.Student')),
                ('notifications', models.ManyToManyField(to='socialnetwork.Notification')),
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
                ('name', models.CharField(max_length=40, blank=True)),
                ('start_time', models.DateTimeField(auto_now_add=True)),
                ('end_time', models.DateTimeField(auto_now_add=True)),
                ('active', models.BooleanField(default=True)),
                ('course', models.CharField(max_length=10)),
                ('location_name', models.CharField(max_length=255, null=True, blank=True)),
                ('location_latitude', models.DecimalField(default=40.4430939, null=True, max_digits=30, decimal_places=20, blank=True)),
                ('location_longitude', models.DecimalField(default=-79.942309, null=True, max_digits=30, decimal_places=20, blank=True)),
                ('private', models.BooleanField(default=False)),
                ('classroom', models.ForeignKey(related_name='classroom', to='socialnetwork.Classroom')),
                ('members', models.ManyToManyField(related_name='groups', to='socialnetwork.Student')),
                ('owner', models.ForeignKey(related_name='studygroups', to='socialnetwork.Student')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='post',
            name='downvoters',
            field=models.ManyToManyField(related_name='downvoted', to='socialnetwork.Student'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='post',
            name='student',
            field=models.ForeignKey(to='socialnetwork.Student'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='post',
            name='studygroup',
            field=models.ForeignKey(related_name='posts', to='socialnetwork.StudyGroup', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='post',
            name='upvoters',
            field=models.ManyToManyField(related_name='upvoted', to='socialnetwork.Student'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='documents',
            name='owner',
            field=models.OneToOneField(to='socialnetwork.Student'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='student',
            field=models.ForeignKey(to='socialnetwork.Student', null=True),
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
            field=models.ManyToManyField(related_name='classes', to='socialnetwork.Student'),
            preserve_default=True,
        ),
    ]
