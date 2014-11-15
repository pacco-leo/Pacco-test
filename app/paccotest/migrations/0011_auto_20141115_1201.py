# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paccotest', '0010_plateforminfos'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='PlateformInfos',
            new_name='PlateformInfo',
        ),
    ]
