# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('socialnetwork', '0003_auto_20150331_0546'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='classroom',
            name='posts',
        ),
        migrations.AddField(
            model_name='post',
            name='classroom',
            field=models.ForeignKey(to='socialnetwork.Classroom', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='post',
            name='group_name',
            field=models.CharField(max_length=40, blank=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='studygroup',
            name='name',
            field=models.CharField(max_length=40, blank=True),
            preserve_default=True,
        ),
    ]
