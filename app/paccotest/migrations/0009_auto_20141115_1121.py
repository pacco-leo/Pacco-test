# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('paccotest', '0008_useranswer_question'),
    ]

    operations = [
        migrations.RenameField(
            model_name='question',
            old_name='order_index',
            new_name='order',
        ),
    ]
