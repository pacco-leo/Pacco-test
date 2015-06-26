# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=200)),
                ('text_en', models.CharField(max_length=200, null=True)),
                ('text_fr', models.CharField(max_length=200, null=True)),
                ('text_nl', models.CharField(max_length=200, null=True)),
                ('order', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CalibrationMemo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('date_calibration', models.DateTimeField(auto_now=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CalibrationSteps',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('sentence', models.CharField(max_length=300, verbose_name=b'sentence')),
                ('command', models.CharField(max_length=300, verbose_name=b'command')),
                ('delay', models.IntegerField()),
                ('tempCompensation', models.BooleanField(default=False)),
                ('order', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='PlateformInfo',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('software_version', models.FloatField()),
                ('rpi_id', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Probe',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('text', models.CharField(max_length=200, verbose_name=b'text')),
                ('text_en', models.CharField(max_length=200, null=True, verbose_name=b'text')),
                ('text_fr', models.CharField(max_length=200, null=True, verbose_name=b'text')),
                ('text_nl', models.CharField(max_length=200, null=True, verbose_name=b'text')),
                ('channel', models.IntegerField()),
                ('calibrable', models.BooleanField(default=True)),
                ('criterable', models.BooleanField(default=True)),
                ('order', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='ProbeMeasure',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('measure', models.CharField(max_length=200, verbose_name=b'measure')),
                ('probeType', models.ForeignKey(to='paccotest.Probe')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Question',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('text', models.CharField(max_length=300, verbose_name=b'text')),
                ('text_en', models.CharField(max_length=300, null=True, verbose_name=b'text')),
                ('text_fr', models.CharField(max_length=300, null=True, verbose_name=b'text')),
                ('text_nl', models.CharField(max_length=300, null=True, verbose_name=b'text')),
                ('order', models.IntegerField()),
                ('actif', models.BooleanField(default=True)),
                ('answers', models.ManyToManyField(to='paccotest.Answer')),
            ],
            options={
                'ordering': ['order'],
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Survey',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('latitude', models.FloatField(verbose_name=b'latitude')),
                ('longitude', models.FloatField(verbose_name=b'longitude')),
                ('elevation', models.FloatField(verbose_name=b'elevation')),
                ('utc', models.DateTimeField(verbose_name=b'date')),
                ('uploadedToServer', models.BooleanField(default=False, verbose_name=b'uploadedToServer')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='UserAnswer',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('answer', models.ForeignKey(to='paccotest.Answer')),
                ('question', models.ForeignKey(to='paccotest.Question')),
                ('survey', models.ForeignKey(to='paccotest.Survey')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WaterCategorie',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=200)),
                ('text', models.CharField(max_length=200, verbose_name=b'text')),
                ('text_en', models.CharField(max_length=200, null=True, verbose_name=b'text')),
                ('text_fr', models.CharField(max_length=200, null=True, verbose_name=b'text')),
                ('text_nl', models.CharField(max_length=200, null=True, verbose_name=b'text')),
                ('order', models.IntegerField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='WaterCategoriesValue',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('valueMax', models.DecimalField(max_digits=10, decimal_places=2)),
                ('valueMin', models.DecimalField(max_digits=10, decimal_places=2)),
                ('probeType', models.ForeignKey(to='paccotest.Probe')),
                ('waterCategorie', models.ForeignKey(to='paccotest.WaterCategorie')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='probemeasure',
            name='survey',
            field=models.ForeignKey(to='paccotest.Survey'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='calibrationsteps',
            name='probeType',
            field=models.ForeignKey(to='paccotest.Probe'),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='calibrationmemo',
            name='probeType',
            field=models.ForeignKey(to='paccotest.Probe', unique=True),
            preserve_default=True,
        ),
    ]
