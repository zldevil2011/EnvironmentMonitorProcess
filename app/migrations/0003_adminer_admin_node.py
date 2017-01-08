# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0002_auto_20161124_0934'),
    ]

    operations = [
        migrations.AddField(
            model_name='adminer',
            name='admin_node',
            field=models.CommaSeparatedIntegerField(max_length=500, null=True),
        ),
    ]
