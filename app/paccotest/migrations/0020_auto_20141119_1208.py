# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paccotest', '0019_auto_20141119_1148'),
    ]

    operations = [
        migrations.RenameField(
            model_name='answer',
            old_name='answer_text',
            new_name='text',
        ),
        migrations.RemoveField(
            model_name='question',
            name='title',
        ),
        migrations.AddField(
            model_name='answer',
            name='text_en',
            field=models.CharField(max_length=200, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='answer',
            name='text_fr',
            field=models.CharField(max_length=200, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='answer',
            name='text_nl',
            field=models.CharField(max_length=200, null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='probe',
            name='text',
            field=models.CharField(default='text', max_length=200, verbose_name=b'text'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='probe',
            name='text_en',
            field=models.CharField(max_length=200, null=True, verbose_name=b'text'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='probe',
            name='text_fr',
            field=models.CharField(max_length=200, null=True, verbose_name=b'text'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='probe',
            name='text_nl',
            field=models.CharField(max_length=200, null=True, verbose_name=b'text'),
            preserve_default=True,
        ),
    ]
