# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('socialnetwork', '0002_auto_20150422_0936'),
    ]

    operations = [
        migrations.AlterField(
            model_name='notification',
            name='link',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='notification',
            name='no_link',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
        migrations.AlterField(
            model_name='notification',
            name='text',
            field=models.CharField(max_length=200, blank=True),
        ),
        migrations.AlterField(
            model_name='notification',
            name='yes_link',
            field=models.CharField(max_length=200, null=True, blank=True),
        ),
    ]
