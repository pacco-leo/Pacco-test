# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paccotest', '0012_survey_uploadedtoserver'),
    ]

    operations = [
        migrations.AlterField(
            model_name='survey',
            name='uploadedToServer',
            field=models.BooleanField(default=False),
        ),
    ]
