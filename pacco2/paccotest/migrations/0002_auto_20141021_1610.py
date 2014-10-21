# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paccotest', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('token', models.IntegerField(verbose_name=b'token')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserAnswer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('survey', models.ForeignKey(to='paccotest.Survey')),
                ('userAnswer', models.ForeignKey(to='paccotest.Answer')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='gpsmeasure',
            name='survey',
            field=models.ForeignKey(default=123, to='paccotest.Survey'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='probemeasure',
            name='survey',
            field=models.ForeignKey(default=345, to='paccotest.Survey'),
            preserve_default=False,
        ),
    ]
