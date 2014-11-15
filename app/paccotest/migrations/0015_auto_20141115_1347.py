# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paccotest', '0014_auto_20141115_1346'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survey',
            name='uploadedToServer',
            field=models.BooleanField(verbose_name=b'uploadedToServer'),
        ),
    ]
