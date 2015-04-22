# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('socialnetwork', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='student',
            name='notifications',
        ),
        migrations.AddField(
            model_name='notification',
            name='student',
            field=models.ForeignKey(related_name='notifications', to='socialnetwork.Student', null=True),
        ),
    ]
