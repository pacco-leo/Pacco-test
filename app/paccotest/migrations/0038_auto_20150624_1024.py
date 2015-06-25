# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paccotest', '0037_auto_20150623_1606'),
    ]

    operations = [
        migrations.AddField(
            model_name='probe',
            name='id',
            field=models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='probe',
            name='channel',
            field=models.IntegerField(),
        ),
    ]
