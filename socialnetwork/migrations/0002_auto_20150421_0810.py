# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('socialnetwork', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='studygroup',
            name='description',
        ),
        migrations.RemoveField(
            model_name='studygroup',
            name='location_room',
        ),
        migrations.RemoveField(
            model_name='studygroup',
            name='topic',
        ),
    ]
