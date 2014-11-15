# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paccotest', '0004_auto_20141024_1630'),
    ]

    operations = [
        migrations.CreateModel(
            name='Probe',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('channel', models.IntegerField()),
                ('order', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.RenameField(
            model_name='probemeasure',
            old_name='mesure',
            new_name='measure',
        ),
        migrations.AlterField(
            model_name='probemeasure',
            name='probeType',
            field=models.ForeignKey(to='paccotest.Probe'),
        ),
        migrations.DeleteModel(
            name='ProbeType',
        ),
    ]
