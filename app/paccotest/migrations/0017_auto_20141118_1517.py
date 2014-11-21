# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paccotest', '0016_auto_20141115_1347'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='question',
            name='question_text',
        ),
        migrations.AddField(
            model_name='question',
            name='text_en',
            field=models.CharField(default='title', max_length=300),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='question',
            name='text_fr',
            field=models.CharField(default='title', max_length=300),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='question',
            name='text_nl',
            field=models.CharField(default='title', max_length=300),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='question',
            name='title',
            field=models.CharField(default='title', max_length=100),
            preserve_default=False,
        ),
    ]
