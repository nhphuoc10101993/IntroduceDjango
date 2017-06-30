# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0003_auto_20170624_2240'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filestorage',
            name='images',
            field=models.ImageField(help_text=b'Please input image dir', upload_to=b'photo/', blank=True),
        ),
    ]
