# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('socialnetwork', '0002_auto_20150421_0810'),
    ]

    operations = [
        migrations.AlterField(
            model_name='studygroup',
            name='location_name',
            field=models.CharField(max_length=255, null=True, blank=True),
        ),
    ]
