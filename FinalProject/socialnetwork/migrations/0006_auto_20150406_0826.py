# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('socialnetwork', '0005_auto_20150406_0734'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='upvotes',
            field=models.IntegerField(default=0, blank=True),
            preserve_default=True,
        ),
    ]
