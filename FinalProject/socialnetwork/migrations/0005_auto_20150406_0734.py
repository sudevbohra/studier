# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('socialnetwork', '0004_auto_20150406_0513'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='classroom',
            field=models.ForeignKey(related_name='posts', to='socialnetwork.Classroom', null=True),
            preserve_default=True,
        ),
    ]
