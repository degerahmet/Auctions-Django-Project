# Generated by Django 3.1 on 2020-08-21 15:06

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('auctions', '0006_auto_20200821_1746'),
    ]

    operations = [
        migrations.AddField(
            model_name='comment',
            name='commentTitle',
            field=models.CharField(default=1, max_length=64),
            preserve_default=False,
        ),
    ]