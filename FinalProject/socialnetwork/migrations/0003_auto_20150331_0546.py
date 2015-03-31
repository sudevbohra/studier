# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('socialnetwork', '0002_auto_20150331_0324'),
    ]

    operations = [
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('location', models.CharField(max_length=40, blank=True)),
                ('text', models.CharField(max_length=160)),
                ('date', models.DateTimeField(auto_now_add=True)),
                ('upvotes', models.IntegerField(blank=True)),
                ('comments', models.ManyToManyField(to='socialnetwork.Comment')),
                ('student', models.ForeignKey(to='socialnetwork.Student')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RemoveField(
            model_name='classroom',
            name='comments',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='answer',
        ),
        migrations.RemoveField(
            model_name='comment',
            name='question',
        ),
        migrations.AddField(
            model_name='classroom',
            name='name',
            field=models.CharField(max_length=40, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='classroom',
            name='posts',
            field=models.ManyToManyField(to='socialnetwork.Post'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='date',
            field=models.DateTimeField(auto_now_add=True, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='student',
            field=models.ForeignKey(to='socialnetwork.Student', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='comment',
            name='text',
            field=models.CharField(max_length=160, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='documents',
            name='name',
            field=models.CharField(max_length=40, blank=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='comment',
            name='upvotes',
            field=models.IntegerField(default=0, blank=True),
            preserve_default=True,
        ),
    ]
