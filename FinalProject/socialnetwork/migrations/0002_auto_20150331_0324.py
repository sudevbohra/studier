# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('socialnetwork', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='classroom',
            name='students',
            field=models.ManyToManyField(related_name='classes', to='socialnetwork.Student'),
            preserve_default=True,
        ),
    ]
